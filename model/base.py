#!/usr/bin/env python
# -*- coding:utf-8 -*-
from peewee import Model, PrimaryKeyField, BigIntegerField
from conn.postgre import PostgresqlClient


class PostgreBaseModel(Model):

    id = PrimaryKeyField()
    create_time = BigIntegerField()
    update_time = BigIntegerField()

    class Meta:
        # table_name = 'name'  # 继承者定义
        database = PostgresqlClient().connect()
        legacy_table_names = False  # 4.0 开始默认就是 False
        # class UserProfile True 生成表: userprofile, False: user_profile
