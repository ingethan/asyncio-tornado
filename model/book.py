#!/usr/bin/env python
# -*- coding:utf-8 -*-
from peewee import PrimaryKeyField, CharField, DecimalField, BigIntegerField, SmallIntegerField
from .base import PostgreBaseModel


class Book(PostgreBaseModel):
    title = CharField(max_length=64, unique=True)
    author = CharField(max_length=64)
    publisher = CharField(max_length=64)
    price = DecimalField(max_digits=10, decimal_places=2)
    desc = CharField(max_length=256)

    class Meta:
        table_name = 'book'
