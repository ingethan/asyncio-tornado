#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tornado import web
from tornado import httpserver
from router import routers
from conn.redis import RedisClient
from conn.mongo import MongoClient
from conn.rabbitmq import RabbitMQClient
from config import PORT, LOOP


def make_app():
    _app = web.Application(handlers=routers)
    _app.redis = RedisClient().connect()
    _app.mongo = MongoClient().connect()
    _app.amqp = RabbitMQClient().connect()
    return _app


if __name__ == '__main__':
    app = make_app()
    # http_server = httpserver.HTTPServer(app)
    # http_server.bind(PORT)
    # http_server.start(num_processes=0)  # win下不可用
    app.listen(PORT)
    LOOP.run_forever()
