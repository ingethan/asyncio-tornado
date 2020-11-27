#!/usr/bin/env python
# -*- coding:utf-8 -*-
from config import REDIS_URI, AMQP_URI


broker_url = AMQP_URI
result_backend = REDIS_URI

timezone = 'Asia/Shanghai'
result_expires = 3600             # Default: 1 day (int seconds, or a timedelta object)

worker_concurrency = 4            # Default: Number of CPU cores
worker_prefetch_multiplier = 4    # Default: 4

# task绑定queue进行监听处理
task_routes = {
    'celery_app.task.fib': {
        'queue': 'aio-queue',
        # 'routing_key': 'aio-routing-key'
    },
}

# 指定任务模块
imports = [
    'celery_app.task',
]
