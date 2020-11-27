#!/usr/bin/env python
# -*- coding:utf-8 -*-
from peewee_async import Manager
from peewee_async import PooledPostgresqlDatabase
from config import POSTGRESQL_CONN, LOOP


class PostgresqlClient:

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            print(f'--- not {cls.__name__}._instance, {cls.__name__}.__new__()')
            cls._conn = PooledPostgresqlDatabase(**POSTGRESQL_CONN)
            cls._manager = Manager(cls._conn, loop=LOOP)
            cls._instance = super(PostgresqlClient, cls).__new__(cls)
        return cls._instance

    def connect(self):
        print(f'--- {self.__class__.__name__}.connect()...')
        return self._conn

    @property
    def manager(self):
        return self._manager
