#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .base import BaseHandler
from service.product import ProductService


class ProductHandler(BaseHandler):

    async def get(self):
        """
        有 id 字段查询单调数据, 没有则查询多条数据
        :return:
        """
        id_ = self.get_argument('id', None)
        if id_:
            result =  await ProductService.find_by_id(self.mongo.product_info, id_)
            return self.finish(result)
        else:
            page = self.get_argument('page', '1')
            page = int(page) if page.isdigit() else 1
            per = self.get_argument('per', '20')
            per = int(per) if per.isdigit() else 20
            where = {}
            catalog = self.get_argument('cat', None)
            if catalog:
                where['catalog'] = catalog
            brand = self.get_argument('brand', None)
            sort = ('update_time', -1)
            _sort = self.get_argument('sort', '')
            if _sort.endswith('_asc') or _sort.endswith('_desc'):
                k, v = _sort.rsplit('_', 1)
                v = 1 if v == 'asc' else -1
                sort = (k, v)
            if brand:
                where['brand'] = brand
            result = await ProductService.find(
                collection=self.mongo.product_info,
                fields=['title', 'catalog', 'brand', 'thumbnail', 'price', 'discount', 'star', 'sold'],
                where=where,
                page=page,
                per=per,
                sort=sort
            )
            return self.finish(result)
