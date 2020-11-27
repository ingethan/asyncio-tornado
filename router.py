#!/usr/bin/env python
# -*- coding:utf-8 -*-
from handler.redis import RedisHandler
from handler.amqp import AMQPFibHandler, AMQPUpperHandler
from handler.user import UserHandler, LoginHandler
from handler.product import ProductHandler
from handler.book import BookHandler


routers = [    
    (r'/api/redis', RedisHandler),
    (r'/api/amqp/fib', AMQPFibHandler),
    (r'/api/amqp/upper', AMQPUpperHandler),

    (r'/api/user', UserHandler),
    (r'/api/login', LoginHandler),
    (r'/api/product', ProductHandler),
    (r'/api/book', BookHandler),
]
