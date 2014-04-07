#coding:utf-8
from __future__ import unicode_literals

import json
from datetime import datetime

import tornado.web

from models import Message, User
from handlers import BaseHandler, USER_CACHE


class MessageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        topic_id = self.get_argument('topic_id')
        if topic_id:
            messages = Message.get_by_topic(topic_id) or []
        else:
            messages = Message.get_all()

        result = []
        current_user_id = self.get_current_user().id
        for m in messages:
            try:
                user = USER_CACHE[m.user_id]
            except KeyError:
                user = User.get_by_id(m.user_id)
                USER_CACHE[m.user_id] = user
            message = dict(m)
            message['user_name'] = user.username
            message['is_mine'] = (current_user_id == user.id)
            result.append(message)
        self.write(json.dumps(result))
        return

    @tornado.web.authenticated
    def POST(self):
        data = self.request.body
        data = json.loads(data)
        user = self.get_current_user()
        if not user:
            self.set_status(400)
            self.write('请先登录')
            return

        message_data = {
            "content": data.get("content"),
            "topic_id": data.get("topic_id"),
            "user_id": user.id,
            "created_time": datetime.now(),
        }
        m_id = Message.create(**message_data)
        result = {
            "id": m_id,
            "content": message_data.get("content"),
            "topic_id": message_data.get("topic_id"),
            "user_id": user.id,
            "user_name": user.username,
            "created_time": str(message_data.get("created_time")),
            "is_mine": True,
        }
        self.write(json.dumps(result))
        return
