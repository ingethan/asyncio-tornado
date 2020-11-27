#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import asyncio


_args = sys.argv
PORT = int(_args[1]) if len(_args) > 1 and _args[1].strip().isdigit() else 8000

REDIS_URI = 'redis://127.0.0.1:6379'

MONGO_URI = 'mongodb://ethaning:Web1982315@120.24.47.175:27017'

AMQP_URI = 'amqp://guest:guest@localhost/my_vhost'

POSTGRESQL_CONN = dict(
    database='exampledb',
    host='120.24.47.175',
    port=5432,
    user='ethaning',
    password='Web1982315',
    min_connections=1,  # default
    max_connections=20  # default
)

JWT_KEY = 'D0670264BBC011E8AE8A8E1578F33B5D'

LOOP = asyncio.get_event_loop()

TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
