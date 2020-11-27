#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .base import BaseHandler
from util.return_retult import JsonReturn


class RedisHandler(BaseHandler):

    async def get(self):
        key = self.get_argument('key', None)
        if key:
            async with self.redis.get() as conn:
                data = await conn.execute('get', key)
                return self.write(JsonReturn.success(data=data))
        else:
            return self.write(JsonReturn.failure(1, 'Missing argument: [ key ]'))

    async def post(self):
        if self.data:
            async with self.redis.get() as conn:
                await conn.execute('set', self.data.get('key'), self.data.get('value'), 'EX', 3600)
                return self.write(JsonReturn.success())
        else:
            return self.write(JsonReturn.failure(1, 'Missing data: {key: string, value: json_obj}'))
