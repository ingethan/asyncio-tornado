#!/usr/bin/env python
# -*- coding:utf-8 -*-
import asyncio
from aiohttp import ClientSession
from datetime import datetime
import json


REQ_URL = 'http://localhost:8000/{path}'
REQ_HEADERS = {'content-type': 'application/json; charset=utf-8'}


async def get(url, params=None, headers=REQ_HEADERS):
    async with ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as resp:
            if resp.status == 200:
                print(f'{resp.status}:', await resp.json())
            else:
                print(f'{resp.status}: Error')


async def post(url, data, params=None, headers=REQ_HEADERS):
    async with ClientSession() as session:
        async with session.post(url, json=data, params=params, headers=headers) as resp:
            if resp.status == 200:
                print(f'{resp.status}:', await resp.json())
            else:
                print(f'{resp.status}: Error')

async def main():
    books = ['红楼梦', '	活着', '百年孤独', '1984', '飘', '三体全集 : 地球往事三部曲', '白夜行',
             '福尔摩斯探案全集（上中下）', '八百万种死法', '聋哑时代']
    tasks = [post(url=REQ_URL.format(path='api/pg/book'), data={'title': i}) for i in books]
    # for i in range(1, 20):
    #     tasks.append(post(url=REQ_URL.format(path='api/amqp/fib'), data={'args': [i], 'task': 'celery_app.task.fib'}))
    await asyncio.wait(tasks)


start = datetime.now()
print(f'>>> start {start.strftime("%H:%M:%S.%f")}')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

end = datetime.now()
print(f'>>> finish {end.strftime("%H:%M:%S.%f")} >>> cost: {end - start}')
