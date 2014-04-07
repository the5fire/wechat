#coding:utf-8

from handlers import BaseHandler


class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html')
