#coding:utf-8
import copy
import json
import hashlib
import sqlite3
from datetime import datetime

import web
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin

from models import Message, User, Topic

session = web.config._session

CACHE_USER = {}


def sha1(data):
    return hashlib.sha1(data).hexdigest()


def bad_request(message):
    raise web.BadRequest(message=message)


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
    def GET(self):
        session.login = False
        session.user = None
        session.kill()
        return web.tempredirect('/#login')


class TopicHandler:
    def GET(self, pk=None):
        if pk:
            topic = Topic.get_by_id(pk)
            return json.dumps(topic)

        topics = Topic.get_all()
        result = []
        for t in topics:
            topic = dict(t)
            try:
                user = CACHE_USER[t.owner_id]
            except KeyError:
                user = User.get_by_id(t.owner_id)
                CACHE_USER[t.owner_id] = user
            topic['owner_name'] = user.username
            result.append(topic)
        return json.dumps(result)

    def POST(self):
        if not session.user or not session.user.id:
            return bad_request('请先登录！')
        if session.user.username != 'the5fire':
            return bad_request('sorry，你没有创建权限')

        data = web.data()
        data = json.loads(data)

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
        current_user_id = session.user.id
        for m in messages:
            try:
                user = CACHE_USER[m.user_id]
            except KeyError:
                user = User.get_by_id(m.user_id)
                CACHE_USER[m.user_id] = user
            message = dict(m)
            message['user_name'] = user.username
            message['is_mine'] = (current_user_id == user.id)
            result.append(message)
        return json.dumps(result)

    def POST(self):
        data = web.data()
        data = json.loads(data)
        if not (session.user and session.user.id):
            return bad_request("请先登录！")

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


class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def on_go_out(self):
        room_num = self.socket.session.get('room')
        if room_num:
            print 'go_out', room_num
            self.leave(room_num)

    def on_topic(self, topic_id):
        """ 加入以某个主题id为房间

        客户端进入聊天室界面先发送此请求，确定房间号
        """
        room_num = 'room_%s' % topic_id
        self.socket.session['room'] = room_num
        print 'join', room_num
        self.join(room_num)

    def on_message(self, model):
        user = self.environ['user']
        if user is None:
            # 手动从store中取出user
            session_id = self.environ['session_id']
            _data = session.store[session_id]
            user = _data['user']
        model.update({
            "user_id": user.id,
            "created_time": datetime.now(),
        })
        m_id = Message.create(**model)
        model.update({
            "user_name": user.username,
            'id': m_id,
            'created_time': str(model['created_time']),
            'is_mine': True,
        })
        # 发送回客户端
        self.emit('message', model)

        # 发送给其他人
        model['is_mine'] = False
        self.emit_to_room(
            self.socket.session['room'],
            'message',
            model,
        )

    def recv_disconnect(self):
        print 'DISCONNECT!!!!!!!!!!!!!!!!!!!!!!!'
        self.disconnect(silent=True)


class SocketHandler:
    def GET(self):
        context = copy.copy(web.ctx.environ)
        context.update({
            "user": session.user,
            "session_id": session.session_id,
        })
        socketio_manage(context, {'': ChatNamespace})
        # 重新载入session数据，因为session在socket请求中改变了
        session._load()
