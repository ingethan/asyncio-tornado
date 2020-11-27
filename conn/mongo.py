#!/usr/bin/env python
# -*- coding:utf-8 -*-
import motor.motor_asyncio
from config import MONGO_URI
from config import LOOP


async def _create_mongo_pool():
    return motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)


class MongoClient:

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            print(f'--- not {cls.__name__}._instance, {cls.__name__}.__new__()')
            cls._mongo = LOOP.run_until_complete(_create_mongo_pool())
            cls._instance = super(MongoClient, cls).__new__(cls)
        return cls._instance

    def connect(self):
        print(f'--- {self.__class__.__name__}.connect()...')
        return self._mongo
