#!/usr/bin/env python
# -*- coding:utf-8 -*-
import aioredis
from config import REDIS_URI
from config import LOOP


async def _create_redis_pool(loop):
    return await aioredis.create_pool(REDIS_URI, encoding='utf-8', loop=loop)


class RedisClient:

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            print(f'--- not {cls.__name__}._instance, {cls.__name__}.__new__()')
            cls._redis = LOOP.run_until_complete(_create_redis_pool(LOOP))
            cls._instance = super(RedisClient, cls).__new__(cls)
        return cls._instance

    def connect(self) -> aioredis.Redis:
        print(f'--- {self.__class__.__name__}.connect()...')
        return self._redis
