#coding:utf-8

from handlers.index import IndexHandler
from handlers.topic import TopicHandler
from handlers.user import LoginHandler, UserHandler, LogoutHandler
from handlers.message import MessageHandler


urls = [
    (r'/', IndexHandler),
    (r'/topic', TopicHandler),
    (r'/topic/(\d+)', TopicHandler),
    (r'/message', MessageHandler),
    (r'/user', UserHandler),
    (r'/user/(\d+)', UserHandler),
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    #(r'/socket.io/.*', SocketHandler),
]
