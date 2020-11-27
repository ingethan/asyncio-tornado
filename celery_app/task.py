#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .app import app
import time
from datetime import datetime
from random import randint


def count_fib(n):
    if n in (0, 1):
        return n
    return count_fib(n - 1) + count_fib(n - 2)


@app.task
def fib(num):
    start = datetime.now()
    time.sleep(randint(1, 5))
    res = count_fib(num)
    finish = datetime.now()
    return dict(
        task='celery_app.task.fib',
        num=num,
        result=res,
        time_cost=str(finish - start)
    )


@app.task
def upper(word):
    """
    测试tornado直接调用并等待返回结果(celery.task可以被app导入), 设定需要计算1-5秒
    :param word: string
    :return:     dict
    """
    time_format = '%Y-%m-%d %H:%M:%S.%f'
    start = datetime.now()
    time.sleep(randint(1, 5))
    finish = datetime.now()
    return dict(
        task='celery_app.task.upper',
        word=word,
        result=word.upper(),
        start=start.strftime(time_format),
        finish=finish.strftime(time_format),
        time_cost=str(finish - start)
    )


"""
结果会写入到 result_backend 格式:
key = celery-task-meta-{task_id}
result = Function return
e.g.
"{
"status": "SUCCESS",
"result": {"key-1": "value-1", "key-2": "value-2"},
"traceback": null,
"children": [],
"task_id": "48e6d144-22c9-4300-b3d9-966238563666",
"date_done": "2019-12-08T15:02:21.703133"
}"
"""