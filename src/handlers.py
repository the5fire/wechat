#coding:utf-8
from __future__ import absolute_import

import os
import json
import hashlib
from datetime import datetime

import web
from jinja2 import Environment, FileSystemLoader

from models import Message, User, Topic

RUN_PATH = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(RUN_PATH, 'templates')

loader = FileSystemLoader(TEMPLATE_PATH)
lookup = Environment(loader=loader)

session = web.config._session


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
            result = json.dumps({'message': '两次密码输入不一致'})
            raise web.HTTPError(status=400, data=result)

        user_data = {
            "username": username,
            "password": hashlib.sha1(password).hexdigest(),
            "registed_time": datetime.now(),
        }

        user_id = User.create(**user_data)

        result = {
            'user_id': user_id,
            'username': username,
        }
        return json.dumps(result)


class LoginHandler:
    def POST(self):
        pass


class LogoutHandler:
    def POST(self):
        session.login = False
        return json.dumps({"message": "success"})


class TopicHandler:
    def GET(self):
        result = {}
        return json.dumps(result)

    def POST(self):
        data = web.data()
        print data

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
