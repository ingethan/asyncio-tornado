#!/usr/bin/env python
# -*- coding:utf-8 -*-
from celery import Celery
from . import config


app = Celery('celery_app')
app.config_from_object(config)
