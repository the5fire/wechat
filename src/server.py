#!/usr/bin/env python
#coding:utf-8
from __future__ import absolute_import

import web

urls = (
    '/', 'IndexHandler',  # 返回首页
    '/topic', 'TopicHandler',
    '/message', 'MessageHandler',
    '/registe', 'RegisteHandler',
    '/login', 'LoginHandler',
    '/logout', 'LogoutHandler',
)

app = web.application(urls, globals())
from web.httpserver import StaticMiddleware
application = app.wsgifunc(StaticMiddleware)

if web.config.get('_session') is None:
    session = web.session.Session(
        app,
        web.session.DiskStore('sessions'),
        initializer={'login': False}
    )
    web.config._session = session

from handlers import (  # NOQA
    IndexHandler,
    LoginHandler, LogoutHandler, RegisteHandler,
    TopicHandler, MessageHandler
)


def main():
    app.run()

if __name__ == "__main__":
    main()
