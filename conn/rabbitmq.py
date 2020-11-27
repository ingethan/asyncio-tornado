#!/usr/bin/env python
# -*- coding:utf-8 -*-
import aio_pika
from aio_pika.pool import Pool
from config import AMQP_URI
from config import LOOP


async def _create_amqp(_loop):
    """
    :param _loop:  event loop
    :return:       返回连接池和channel连接池, 主要使用后者
    """

    async def get_connection():
        return await aio_pika.connect_robust(AMQP_URI)
    connection_pool = Pool(get_connection, max_size=2, loop=_loop)

    async def get_channel():
        async with connection_pool.acquire() as connection:
            return await connection.channel()
    channel_pool = Pool(get_channel, max_size=10, loop=_loop)

    return connection_pool, channel_pool


class RabbitMQClient:

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            print(f'--- not {cls.__name__}._instance, {cls.__name__}.__new__()')
            cls._amqp = LOOP.run_until_complete(_create_amqp(LOOP))
            cls._instance = super(RabbitMQClient, cls).__new__(cls)
        return cls._instance

    def connect(self):
        print(f'--- {self.__class__.__name__}.connect()...')
        return self._amqp

