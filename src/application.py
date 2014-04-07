#coding:utf-8
import os

import tornado.web

from urls import urls


secret_key = '12n+k6cg*x5e(&qc1875q=df%wpd^h=0e02jbl894m%(%qb108'

SETTINGS = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    #xsrf_cookies=True,
    cookie_secret=secret_key,
    debug=True,
)

application = tornado.web.Application(
    handlers=urls,
    **SETTINGS
)
