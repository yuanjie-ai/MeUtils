#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : client
# @Time         : 2022/9/9 下午5:02
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from jina import Client, Document, DocumentArray

# c = Client(host='grpc://0.0.0.0:8504')
#
#
# print(c.post('/', DocumentArray.empty(1)).texts)
# print(c.post('/e1', DocumentArray.empty(2)).texts)
# print(c.post('/e2', DocumentArray.empty(3)).texts)
#


# r = c.post(
#     '/',
#     inputs=DocumentArray([
#         Document(text='如何更换花呗绑定银行卡'),
#         Document(text='花呗更改绑定银行卡')
#     ])
# )
# print(r.embeddings)

#
# {
#     "data": [
#         {
#             "text": "我在南京"
#         }
#     ]
# }


r = Client(host='grpc://0.0.0.0:8501').post('/encode', [Document(text='我是中国人')] * 5)
