#!/usr/bin/env python
# -*- coding:utf-8 -*-
from peewee import *


PG_SETTING = {
    'host': '120.24.47.175',
    'port': 5432,
    'user': 'ethaning',
    'password': 'Web1982315'
}
DB_NAME = 'exampledb'
database = PostgresqlDatabase(DB_NAME, **PG_SETTING)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        database = database


class Book(BaseModel):
    id = PrimaryKeyField()
    title = CharField(max_length=64, unique=True)
    author = CharField(max_length=64)
    publisher = CharField(max_length=64)
    price = DecimalField(max_digits=10, decimal_places=2)
    desc = CharField(max_length=256)
    create_time = BigIntegerField()
    update_time = BigIntegerField()

    class Meta:
        db_table = 'book'


class User(BaseModel):
    id = PrimaryKeyField()
    email = CharField(max_length=64, unique=True)
    password = CharField(max_length=64)
    name = CharField(max_length=64, unique=True)
    phone = CharField(max_length=11, unique=True, null=True)
    gender = SmallIntegerField(null=True, verbose_name='null-保密 | 1-男 | 0-女')
    avatar = CharField(max_length=256, null=True)
    desc = CharField(max_length=256, null=True)
    birthday = DateField(null=True)
    is_active = BooleanField(default=True)
    is_admin = BooleanField(default=False)
    create_time = BigIntegerField()
    update_time = BigIntegerField()

    class Meta:
        db_table = 'user'
