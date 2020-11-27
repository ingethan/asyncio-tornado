#!/usr/bin/env python
# -*- coding:utf-8 -*-
import jwt
from config import JWT_KEY
import time


headers = {
    'alg': 'HS256',
    'typ': 'JWT'
}


def token_encode(info: dict, exp: int) -> str:
    payload = info
    payload['exp'] = int(time.time() + exp)
    return jwt.encode(
        payload=payload,
        key=JWT_KEY,
        algorithm='HS256',
        headers=headers
    ).decode('utf-8')


def token_decode(token: str) -> dict or None:
    try:
        return jwt.decode(
            jwt=token,
            key=JWT_KEY,
            verify=True,
            algorithm='HS256'
        )
    except jwt.PyJWTError:
        return None
