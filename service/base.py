#!/usr/bin/env python
# -*- coding:utf-8 -*-
from conn.postgre import PostgresqlClient
import math
from util.model_serializable import model_to_json
import time
from util.return_retult import JsonReturn
from bson.objectid import ObjectId


#  Manager 一般多数为直接操作
#  Model   一般操作是返回 query, 需要再执行 execute(), 例如示例中的 find()


class PostgreBaseService:

    model = None       # Model , 继承者定义
    _service = dict()  # dict形式保存Service e.g. {'UserService': UserService()}

    @staticmethod
    def instance(cls):
        """
        生成单例, 所有继承类保存到 _service,
        :param cls:  ChildrenService
        :return:     ChildrenService.instance
        """
        instance = cls._service.get(cls.__name__, None)
        if not instance:
            instance = cls.__new__(cls)
            cls._service.setdefault(cls.__name__, instance)
        return instance

    @property
    def objects(self):
        return PostgresqlClient().manager  # peewee.Manager

    async def find_by_id(self, id_: str) -> dict:
        """
        根据id查找单个数据
        DoesNotExist  不是表示 model 不存在，而是数据库查询不到相关结果
        :param id_:   Model.id
        :return:      json: data=dict(Model)
        """
        try:
            result = await self.objects.get(self.model, id=id_)
            return JsonReturn.success(data=model_to_json(result))
        except self.model.DoesNotExist:
            return JsonReturn.failure(404, f'id={id_} not found')

    async def find(self, limit: int=20, skip: int=0, fields: list=None, filters: dict=None) -> dict:
        """
        查询多项数据, 无结果也显示最小为 1 页
        query.count() 必须在 limit 之前执行, 否则得到的数据是 limit 之后的?
        :param limit:  查找数量, per
        :param skip:   跳过数量, per * page
        :param fields  选择字段, 没有则全部选择
        :param filters 筛选条件
        :return:       json: data={total: 15, page: 1, pages: 2, per: 10, data: []}
        """
        if fields:
            assert isinstance(fields, list)
            query = self.model.select(*[getattr(self.model, field) for field in fields])
        else:
            query = self.model.select()
        if filters:
            assert isinstance(filters, dict)
            for k, v in filters.items():
                query = query.where(getattr(self.model, k) == v)
        total = query.count()
        query = query.limit(limit).offset(skip)
        result = await self.objects.execute(query)
        data = dict(
            total=total,
            pages=math.ceil(total/limit) or 1,
            page=skip / limit + 1,
            per=limit,
            data=model_to_json(result)
        )
        return JsonReturn.success(data=data)

    async def insert_one(self, data: dict) -> dict:
        """
        插入单条数据
        :param data:   dict
        :return:       json: data=dict (insert)
        """
        data['create_time'] = int(time.time())
        data['update_time'] = int(time.time())
        try:
            async with self.objects.atomic():
                result = await self.objects.create(self.model, **data)  # result <class 'peewee.Model'>
            return JsonReturn.success(data=model_to_json(result))
        except Exception as e:
            return JsonReturn.failure(500, e.args[0])

    async def insert_many(self, data: list) -> dict:
        """
        插入多条数据
        :param data: list
        :return:     json data={'count': int}
        """
        for each in data:
            each['create_time'] = int(time.time())
            each['update_time'] = int(time.time())
        query = self.model.insert_many(data)
        try:
            async with self.objects.atomic():
                result = await self.objects.execute(query)  # bool
            if result:
                return JsonReturn.success(data={'count': len(data)})
            else:
                return JsonReturn.failure(500, 'insert fail')
        except Exception as e:
            return JsonReturn.failure(500, e.args[0])

    async def update_by_id(self, id_: str, updater: dict) -> dict:
        """ 更新单条数据
        如果有 update_time 字段, 则自动更新该字段
        :param id_:      id
        :param updater:  dict 需要更新的字段
        :return:         json data={'count': int}
        """
        try:
            updater_ = {getattr(self.model, key): value for key, value in updater.items()}
            updater_[self.model.update_time] = int(time.time())
            query = self.model.update(updater_).where(self.model.id == id_)
            async with self.objects.atomic():
                await self.objects.execute(query)
            return JsonReturn.success()
        except AttributeError as e:
            return JsonReturn.failure(500, e.args[0])
        except Exception as e:
            return JsonReturn.failure(500, e.args[0])

    async def update(self, updater: dict, filters: dict) -> dict:
        """
        更新数据
        :param updater: 更新字段(update) e.g. {'price': 9.9}
        :param filters: 更新条件(where)  e.g. {'price': 10}
        :return:
        """
        assert isinstance(updater, dict)
        assert isinstance(filters, dict)
        _updater = {getattr(self.model, key): value for key, value in updater.items()}
        _updater[self.model.update_time] = int(time.time())
        query = self.model.update(_updater)
        if filters:
            for k, v in filters.items():
                query = query.where(getattr(self.model, k) == v)
        async with self.objects.atomic():
            result = await self.objects.execute(query)
        return JsonReturn.success(data={'count': result})

    async def delete_by_id(self, id_: str) -> dict:
        """
        删除单条数据
        :param id_:
        :return:
        """
        try:
            obj = await self.objects.get(self.model, id=id_)
            async with self.objects.atomic():
                result = await self.objects.delete(obj)
            return JsonReturn.success(data={'count': result})
        except self.model.DoesNotExist:
            return JsonReturn.failure(404, f'id={id_} not exist')
        except Exception as e:
            return JsonReturn.failure(500, e.args[0])

    async def delete(self, filters: dict) -> dict:
        """
        删除多条数据
        :param filters: 删除条件
        :return:
        """
        assert isinstance(filters, dict)
        query = self.model.delete()
        for k, v in filters.items():
            query = query.where(getattr(self.model, k) == v)
        async with self.objects.atomic():
            result = await self.objects.execute(query)  # number of rows removed.
        return JsonReturn.success(data={'count': result})


class MongoBaseService:

    @staticmethod
    async def find_by_id(collection, id_):
        result = await collection.find_one({'_id': ObjectId(id_)})
        print('find_by_id result =', result)
        if result:
            result['id'] = str(result.pop('_id'))
            result['create_time'] = time.strftime(
                                        "%Y-%m-%d %H:%M:%S",
                                        time.localtime(int(result['create_time'] / 1000))  # 坑, 存储毫秒
                                    )
            result['update_time'] = time.strftime(
                                        "%Y-%m-%d %H:%M:%S",
                                        time.localtime(int(result['update_time'] / 1000))  # 坑, 存储毫秒
                                    )
            return JsonReturn.success(data=result)
        else:
            return JsonReturn.failure(404, f'id={id} not found')

    @staticmethod
    async def find(
            collection,
            fields: list=None,
            where: dict=None,
            page: int=1,
            per: int=20,
            sort: tuple=('update_time', -1)
        ):
        """
        查找多条数据
        :param collection: 数据表 <class motor_asyncio.AsyncIOMotorCollection>
        :param fields:     需要查询的字段, 不传全部返回 List  e.g. ['title', 'name']
        :param where:      查询条件 dict       e.g   {'age': 20}
        :param page:       查询页
        :param per:        每页显示条数
        :param sort:       排序条件 tuple 1 升序, -1 降序
        :return:
        """
        if not fields:
            query = collection.find(where if where else {})
        else:
            query = collection.find(where if where else {}, dict.fromkeys(fields, True))
        query = query.sort(*sort).skip((page - 1) * per).limit(per)
        result = await query.to_list(None)
        total = await collection.count_documents(where or {})
        for each in result:
            each['id'] = str(each.pop('_id'))
        return dict(
            total=total,
            pages=math.ceil(total / per) or 1,
            page=page,
            per=per,
            data=result
        )
