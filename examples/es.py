#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : es
# @Time         : 2023/4/14 16:24
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

# /Users/betterme/Downloads/elasticsearch-8.7.0/bin/elasticsearch

# 推荐使用  elasticsearch  需要注意版本问题
from elasticsearch import Elasticsearch

client = Elasticsearch("http://0.0.0.0:9200")
print(client.info) # es信息
#
# 创建索引
result = client.indices.create(index='user')
print(result)
# 删除索引
result = client.indices.delete(index='user')
print(result)
#
# # 更新数据  必须的用
# '''
# 不用doc包裹会报错
# ActionRequestValidationException[Validation Failed: 1: script or doc is missing
# '''
#
# data = {'doc': {'userid': '1', 'username': 'lqz', 'password': '123ee', 'test': 'test'}}
# result = client.update(index='news', doc_type='_doc', body=data, id=1)
# print(result)
#
#
#
# # 查询           查询 原生咋查，这里就可以咋用
# # 查找所有文档
# query = {'query': {'match_all': {}}}
# #  查找名字叫做lxx的所有文档
# query = {'query': {'term': {'name': 'lxx'}}}
# # 查找年龄大于11的所有文档
# query = {'query': {'range': {'price': {'gt': 100}}}}
# allDoc = client.search(index='books',  body=query)
# print(allDoc)
