wechat
==================

An online chat room base on backbonejs &amp; webpy &amp; sqlite3

Css styles Power by `semantic <http://zh.semantic-ui.com/>`_ 

Quick Start
------------------------
You should modify hosts/remote_user or other configration in ``deploy-wechat-simple.yml`` first, then::

    ansible-playbook deploy-wechat-simple.yml

and then: access it via: http://127.0.0.1:9999

Screenshots
---------------------

login:
~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: data/login.png


topics:
~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: data/topics.png


messages:
~~~~~~~~~~~~~~~~~~~~

.. image:: data/chat.png


TODO:
------------------------

1. replace gevent-socketio with tornado.
2. use socketio save message data.
