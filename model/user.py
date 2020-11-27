#!/usr/bin/env python
# -*- coding:utf-8 -*-
from peewee import CharField, DateField, BooleanField, SmallIntegerField
from .base import PostgreBaseModel


class User(PostgreBaseModel):
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

    class Meta:
        table_name = 'user'
