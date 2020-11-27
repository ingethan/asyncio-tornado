#!/usr/bin/env python
# -*- coding:utf-8 -*-
from collections import Iterable
from playhouse.shortcuts import model_to_dict
from decimal import Decimal
import datetime
from config import DATETIME_FORMAT, DATE_FORMAT

# TypeError: Object of type '***' is not JSON serializable


def process(model):
    """
    模型转字典, 处理 'Decimal', 'datetime.datetime', 'datetime.date' 等
    :param model:  peewee.Model
    :return:       dict
    """
    res = model_to_dict(model)
    for k, v in res.items():
        if isinstance(v, Decimal):
            res[k] = float(v)
        elif isinstance(v, datetime.datetime):
            res[k] = v.strftime(DATETIME_FORMAT)
        elif isinstance(v, datetime.date):
            res[k] = v.strftime(DATE_FORMAT)
    return res


def model_to_json(obj):
    if isinstance(obj, Iterable):
        return [process(o) for o in obj]
    else:
        return process(obj)
