#coding:utf-8
from __future__ import unicode_literals

import json
import sqlite3
from datetime import datetime

import tornado.web

from handlers import BaseHandler, USER_CACHE
from models import Topic, User


class TopicHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, pk=None):
        if pk:
            topic = Topic.get_by_id(pk)
            self.write(json.dumps(topic))
            return

        topics = Topic.get_all()
        result = []
        for t in topics:
            topic = dict(t)
            try:
                user = USER_CACHE[t.owner_id]
            except KeyError:
                user = User.get_by_id(t.owner_id)
                USER_CACHE[t.owner_id] = user
            topic['owner_name'] = user.username
            result.append(topic)
        self.write(json.dumps(result))
        return

    @tornado.web.authenticated
    def post(self):
        data = self.request.body
        data = json.loads(data)
        if not self.current_user:
            self.set_status(400)
            self.write('请先登录')
            return

        user = self.current_user
        topic_data = {
            "title": data.get('title'),
            "owner_id": user.id,
            "created_time": datetime.now(),
        }

        try:
            topic_id = Topic.create(**topic_data)
        except sqlite3.IntegrityError:
            self.set_status(400)
            self.write('该名称【%s】已存在' % data.get('title'))
            return

        result = {
            "id": topic_id,
            "title": topic_data.get('title'),
            "owner_id": user.id,
            "owner_name": user.username,
            "created_time": str(topic_data.get('created_time')),
        }
        self.write(json.dumps(result))
        return
