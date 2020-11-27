#!/usr/bin/env python
# -*- coding:utf-8 -*-
from aio_pika import Message
import uuid
import json
from tornado.concurrent import Future
from functools import partial
from util.return_retult import JsonReturn
from .base import BaseHandler
from celery_app.task import upper


class AMQPFibHandler(BaseHandler):

    default_exchange = 'aio-exchange'
    default_routing_key = 'aio-routing-key'
    task_prefix = 'celery-task-meta-'

    async def get(self):
        tid = self.get_argument('tid', None)
        if tid:
            async with self.redis.get() as conn:
                data_str = await conn.execute('get', f'{AMQPFibHandler.task_prefix}{tid}')
                if not data_str:
                    return self.write(JsonReturn.failure(1, 'No result, try again later or check your "tid"'))
                data = json.loads(data_str, encoding='utf-8')
                return self.write(JsonReturn.success(data=data.get('result')))
        else:
            return self.write(JsonReturn.failure(1, 'Missing argument: [ tid ]'))

    async def post(self):
        _data = self.data
        if _data.get('args') and _data.get('task'):
            tid = str(uuid.uuid1()).replace('-', '')
            body = bytes(json.dumps({'id': tid,
                                     'args': _data.get('args'),
                                     'task': _data.get('task')}),
                         encoding='utf8')
            exchange = _data.get('exchange') or AMQPFibHandler.default_exchange
            routing_key = _data.get('routing_key') or AMQPFibHandler.default_routing_key
            async with self.amqp[1].acquire() as channel:
                exchange = await channel.declare_exchange(name=exchange, durable=True)
                await exchange.publish(Message(body=body,
                                               content_type='application/json',
                                               content_encoding='string'),
                                       routing_key=routing_key)
                return self.write(JsonReturn.success(data={'tid': tid}))
        else:
            return self.write(JsonReturn.failure(1, 'data format e.g. {args: [int], task: "celery_app.task.fib"}'))


class AMQPUpperHandler(BaseHandler):

    def wait_result(self, task, future):
        """
        完成执行回调返回结果, 否则扔到当前loop
        :param task:   <class 'celery.result.AsyncResult'>
        :param future: <Future pending cb=[<TaskWakeupMethWrapper object>()]>
        """
        if task.ready():
            future.set_result(task.result)   # task.result 是从 result_backend 中取结果, 不设置的话报错
        else:
            self.amqp[0].loop.call_soon(partial(self.wait_result, task, future))

    async def get(self):
        word = self.get_argument('word', None)
        if not word:
            return self.write(JsonReturn.failure(1, 'Missing argument: <word>'))
        task = upper.delay(word)
        future = Future()
        self.wait_result(task, future)
        res = await future
        task.forget()   # 清除存储的结果
        return self.write(JsonReturn.success(data=res))
