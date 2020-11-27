#!/usr/bin/env python
# -*- coding:utf-8 -*-
import functools
from .jwt_token import token_decode


def verify_user(func):
    """ 用户验证
    request headers 携带有效 jwtoken
    成功: 设置 current_user
    :return : func
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        token = self.request.headers.get('jwtoken')
        if token:
            user = token_decode(token)
            if user:
                self.current_user = user
                return func(self, *args, **kwargs)
            else:
                return self.finish({
                    'err': 500,
                    'smg': 'disabled token'}
                )
        else:
            return self.finish({
                'err': 500,
                'msg': 'missing token'}
            )
    return wrapper


def verify_admin(func):
    """
    verify_user is_admin == True
    :return : func
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.current_user.get('is_admin'):
            return func(self, *args, **kwargs)
        else:
            return self.finish({
                'err': 500,
                'msg': 'you do not have permission'}
            )
    return wrapper
