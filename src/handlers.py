#coding:utf-8
from __future__ import absolute_import

import os
import json
import hashlib
import sqlite3
from datetime import datetime

import web
from jinja2 import Environment, FileSystemLoader

from models import Message, User, Topic

RUN_PATH = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(RUN_PATH, 'templates')

loader = FileSystemLoader(TEMPLATE_PATH)
lookup = Environment(loader=loader)

session = web.config._session


def sha1(data):
    return hashlib.sha1(data).hexdigest()


def bad_request(message):
    result = json.dumps({'message': message})
    raise web.HTTPError(status=400, data=result)


# 首页
class IndexHandler:
    def GET(self):
        t = lookup.get_template('index.html')
        return t.render()


class RegisteHandler:
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

        result = {
            'user_id': user_id,
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
    def GET(self):
        topics = Topic.get_all()
        result = []
        for topic in topics:
            print topic
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
            "created_time": topic_data.get('created_time'),
        }
        return json.dumps(result)

    def PUT(self, obj_id=None):
        data = web.data()
        print data

    def DELETE(self, obj_id=None):
        pass


class MessageHandler:
    def GET(self):
        return json.dumps({})

    def POST(self):
        data = web.data()
        print data
