#coding: utf-8
from __future__ import unicode_literals

from tornado.web import RequestHandler

from models import User

from utils.lru import LRUCacheDict

# 大小为30，超时为3分钟的缓存
USER_CACHE = LRUCacheDict(max_size=30, expiration=3*60)


class BaseHandler(RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("g_user")
        if not user_id:
            return None
        try:
            user = USER_CACHE[user_id]
        except KeyError:
            user = User.get_by_id(user_id)
            USER_CACHE[user_id] = user

        return user
