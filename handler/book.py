#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .base import BaseHandler
from service.book import BookService
from util.return_retult import JsonReturn


class BookHandler(BaseHandler):

    @property
    def service(self) -> BookService:
        return BookService.instance(BookService)

    async def get(self):
        id_ = self.get_argument('id')
        result = await self.service.find_by_id(id_)
        return self.finish(result)

    async def post(self):
        book = self.data
        result = await self.service.insert_one(book)
        return self.finish(result)

    async def put(self):
        id_ = self.get_argument('id')
        updater = self.data
        for k, _ in updater.items():
            if k in ['id', 'create_time', 'update_time']:
                updater.pop(k)
        if not updater:
            return self.finish(JsonReturn.failure(1, 'missing data'))
        result = await self.service.update_by_id(id_, updater)
        return self.finish(result)

    async def delete(self):
        id_ = self.get_argument('id')
        result = await self.service.delete_by_id(id_)
        return self.finish(result)
