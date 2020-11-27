#!/usr/bin/env python
# -*- coding:utf-8 -*-
import jwt
import time
import sys

headers = {
  'alg': 'HS256',
  'typ': 'JWT'
}
# 设置headers，即加密算法的配置
key = 'D0670264BBC011E8AE8A8E1578F33B5D'
# 随机的salt密钥，只有token生成者（同时也是校验者）自己能有，用于校验生成的token是否合法
exp = int(time.time() + 3600*24)
# 设置超时时间：当前时间的1s以后超时
payload = {
    'id': 1012,
    'exp': exp
}
# 配置主体信息，一般是登录成功的用户之类的，因为jwt的主体信息很容易被解码，所以不要放敏感信息
# 当然也可以将敏感信息加密后再放进payload

# 生成token
jwtoken = jwt.encode(payload=payload, key=key, algorithm='HS256', headers=headers).decode('utf-8')
print(f'jwtoken = [{jwtoken}], size = {sys.getsizeof(jwtoken)}bytes')

info = jwt.decode(jwt=jwtoken, key=key, verify=True, algorithm='HS256')
# 解码token，第二个参数用于校验
# 第三个参数代表是否校验，如果设置为False，那么只要有token，就能够对其进行解码
print('正确的 key 进行验证, info =', info)

try:
    info = jwt.decode(jwt=jwtoken, key='123', verify=True, algorithm='HS256')
    print('错误的 key 进行验证, info =', info)
except jwt.PyJWTError as e:
    print(e.args[0])

time.sleep(2)  # 等待2s后再次验证token，因超时将导致验证失败
try:
    info = jwt.decode(jwt=jwtoken, key=key, verify=True, algorithm='HS256')
    print('时间失效后进行验证, info =', info)
except jwt.PyJWTError as e:
    print(e.args[0])
