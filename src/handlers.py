#coding:utf-8
import json
import hashlib
import sqlite3
from datetime import datetime

import web

from models import Message, User, Topic

session = web.config._session


def sha1(data):
    return hashlib.sha1(data).hexdigest()


def bad_request(message):
    return web.BadRequest(message=message)


# 首页
class IndexHandler:
    def GET(self):
        render = web.template.render('templates/')
        return render.index()


class UserHandler:
    def GET(self):
        # 获取当前登录的用户数据
        user = session.user
        return json.dumps(user)

    def POST(self):
        data = web.data()
        data = json.loads(data)
        username = data.get("username")
        password = data.get("password")
        password_repeat = data.get("password_repeat")

        if password != password_repeat:
            return bad_request('两次密码输入不一致')

        user_data = {
            "username": username,
            "password": sha1(password),
            "registed_time": datetime.now(),
        }

        try:
            user_id = User.create(**user_data)
        except sqlite3.IntegrityError:
            return bad_request('用户名已存在!')

        user = User.get_by_id(user_id)
        session.login = True
        session.user = user

        result = {
            'id': user_id,
            'username': username,
        }
        return json.dumps(result)


class LoginHandler:
    def POST(self):
        data = web.data()
        data = json.loads(data)
        username = data.get("username")
        password = data.get("password")
        user = User.get_by_username_password(
            username=username,
            password=sha1(password)
        )
        if not user:
            return bad_request('用户名或密码错误！')

        session.login = True
        session.user = user
        result = {
            'id': user.get('id'),
            'username': user.get('username'),
        }
        return json.dumps(result)


class LogoutHandler:
    def POST(self):
        session.login = False
        session.user = None
        return json.dumps({"message": "success"})


class TopicHandler:
    def GET(self, pk=None):
        if pk:
            topic = Topic.get_by_id(pk)
            return json.dumps(topic)

        topics = Topic.get_all()
        result = []
        for t in topics:
            topic = dict(t)
            user = User.get_by_id(t.owner_id)
            topic['owner_name'] = user.username
            result.append(topic)
        return json.dumps(result)

    def POST(self):
        data = web.data()
        data = json.loads(data)
        if not session.user.id:
            return bad_request('请先登录！')

        topic_data = {
            "title": data.get('title'),
            "owner_id": session.user.id,
            "created_time": datetime.now(),
        }

        try:
            topic_id = Topic.create(**topic_data)
        except sqlite3.IntegrityError:
            return bad_request('你已创建过该名称!')

        result = {
            "id": topic_id,
            "title": topic_data.get('title'),
            "owner_id": session.user.id,
            "owner_name": session.user.username,
            "created_time": str(topic_data.get('created_time')),
        }
        return json.dumps(result)

    def PUT(self, obj_id=None):
        data = web.data()
        print data

    def DELETE(self, obj_id=None):
        pass


class MessageHandler:
    def GET(self):
        topic_id = web.input().get('topic_id')
        if topic_id:
            messages = Message.get_by_topic(topic_id) or []
        else:
            messages = Message.get_all()

        result = []
        for m in messages:
            user = User.get_by_id(m.user_id)
            message = dict(m)
            message['user_name'] = user.username
            message['is_mine'] = (session.user == user)
            result.append(message)
        return json.dumps(result)

    def POST(self):
        data = web.data()
        data = json.loads(data)
        #if not (session.user and session.user.id):
            #return bad_request("请先登录！")

        message_data = {
            "content": data.get("content"),
            "topic_id": data.get("topic_id"),
            "user_id": session.user.id,
            "created_time": datetime.now(),
        }
        m_id = Message.create(**message_data)
        result = {
            "id": m_id,
            "content": message_data.get("content"),
            "topic_id": message_data.get("topic_id"),
            "user_id": session.user.id,
            "user_name": session.user.username,
            "created_time": str(message_data.get("created_time")),
            "is_mine": True,
        }
        return json.dumps(result)
