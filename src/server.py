#!/usr/bin/env python
#coding:utf-8
import web
from web.httpserver import StaticMiddleware

urls = (
    '/', 'IndexHandler',  # 返回首页
    '/topic', 'TopicHandler',
    '/message', 'MessageHandler',
    '/user', 'RegisteHandler',
    '/login', 'LoginHandler',
    '/logout', 'LogoutHandler',
)

app = web.application(urls, globals())
application = app.wsgifunc(StaticMiddleware)

if web.config.get('_session') is None:
    session = web.session.Session(
        app,
        web.session.DiskStore('sessions'),
        initializer={'login': False, 'user': None}
    )
    web.config._session = session

from handlers import (  # NOQA
    IndexHandler, RegisteHandler,
    LoginHandler, LogoutHandler,
    TopicHandler, MessageHandler
)


def main():
    app.run()

if __name__ == "__main__":
    main()
