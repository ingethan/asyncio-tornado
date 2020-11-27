#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .base import BaseHandler
from service.user import UserService
from util.return_retult import JsonReturn
from util.verify_user import verify_user, verify_admin


class UserHandler(BaseHandler):

    @property
    def service(self) -> UserService:
        return UserService.instance(UserService)

    @verify_user
    async def get(self):
        id_ = self.current_user.get('id')
        result = await self.service.find_by_id(id_)
        return self.finish(result)

    async def post(self):
        user = self.data
        result = await self.service.insert_one(user)
        return self.finish(result)

    @verify_user
    async def put(self):
        id_ = self.current_user.get('id')
        updater = self.data
        for k, _ in updater.items():
            if k in ['id', 'create_time', 'update_time', 'is_active', 'is_admin']:
                updater.pop(k)
        if not updater:
            return self.finish(JsonReturn.failure(1, 'missing data'))
        result = await self.service.update_by_id(id_, updater)
        return self.finish(result)

    @verify_admin
    @verify_user
    async def delete(self):
        id_ = self.current_user.get('id')
        result = await self.service.delete_by_id(id_)
        return self.finish(result)


class LoginHandler(BaseHandler):

    @property
    def service(self) -> UserService:
        return UserService.instance(UserService)

    async def post(self):
        email = self.data.get('email')
        password = self.data.get('password') or self.data.get('pw')
        exp = self.data.get('exp') if isinstance(self.data.get('exp'), int) else 3600*24  # 不传有效期则为24小时
        result = await self.service.login(email, password, exp)
        return self.finish(result)

    @verify_user
    async def delete(self):
        result = await self.service.logout()
        return self.finish(result)
