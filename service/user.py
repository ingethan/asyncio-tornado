#!/usr/bin/env python
# -*- coding:utf-8 -*-
from service.base import PostgreBaseService
from model.user import User
from util.return_retult import JsonReturn
import hashlib
from util.jwt_token import token_encode


class UserService(PostgreBaseService):

    model = User

    async def login(self, email, password, exp) -> dict:
        try:
            user = await self.objects.get(self.model, email=email)
            m5 = hashlib.md5()
            m5.update(password.encode(encoding='utf-8'))
            pw = m5.hexdigest()
            print(user.password)
            print(pw)
            if user.password != pw:
                return JsonReturn.failure(1, 'error password')
            payload = {
                'id': user.id,
                'name': user.name,
                'is_admin': user.is_admin
            }
            token = token_encode(payload, exp)
            return JsonReturn.success(data={'jwtoken': token})
        except self.model.DoesNotExist:
            return JsonReturn.failure(404, f'email={email} not found')

    async def logout(self):
        token = token_encode({}, 0)
        return JsonReturn.success(data={'jwtoken': token})
