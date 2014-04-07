#coding:utf-8
from __future__ import unicode_literals

import json
import hashlib
import sqlite3
from datetime import datetime

import tornado.web
from handlers import BaseHandler

from models import User


def sha1(data):
    return hashlib.sha1(data).hexdigest()


class UserHandler(BaseHandler):
    def get(self):
        """ 获取当前登录的用户数据 """
        user = self.current_user
        if user is None:
            user = {}
        self.write(json.dumps(user))
        return

    def post(self):
        """ 注册用户 """
        data = self.request.body
        data = json.loads(data)
        username = data.get("username")
        password = data.get("password")
        password_repeat = data.get("password_repeat")

        if password != password_repeat:
            self.set_status(404)
            self.write('两次密码输入不一致')
            return

        user_data = {
            "username": username,
            "password": sha1(password),
            "registed_time": datetime.now(),
        }

        try:
            user_id = User.create(**user_data)
        except sqlite3.IntegrityError:
            raise tornado.web.HTTPError(400)

        user = User.get_by_id(user_id)

        self.set_secure_cookie("g_user", str(user.get('id')))

        result = {
            'id': user_id,
            'username': username,
        }
        self.write(json.dumps(result))
        return


class LoginHandler(BaseHandler):
    def post(self):
        data = self.request.body
        data = json.loads(data)
        username = data.get("username")
        password = data.get("password")
        user = User.get_by_username_password(
            username=username,
            password=sha1(password)
        )
        if not user:
            self.set_status(400)
            self.write("用户名或密码错误")
            return

        self.set_secure_cookie("g_user", str(user.get('id')))
        result = {
            'id': user.get('id'),
            'username': user.get('username'),
        }
        self.write(json.dumps(result))
        return


class LogoutHandler:
    def GET(self):
        self.clear_cookie("g_user")
        self.redirect('/#login')
        return
