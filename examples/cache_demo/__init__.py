#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : __init__.py
# @Time         : 2021/11/24 上午10:28
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

import time

from operator import attrgetter
from cachetools import TTLCache, LRUCache, RRCache, cachedmethod, cached

cache = TTLCache(maxsize=10, ttl=timedelta(hours=12), timer=datetime.now)

class Model:

    def __init__(self, cachesize):
        self.cache = LRUCache(maxsize=cachesize)

    @cachedmethod(attrgetter('cache'))
    def get_double_num(self, num):
        """ return  2* num"""
        print(f'get_double_num({num})  is running')
        time.sleep(2)
        return num * 2


model = Model(cachesize=10)

print(model.get_double_num(10))
print(model.get_double_num(10))
print(model.get_double_num(10))
print(model.get_double_num(10))
print(model.get_double_num(10))
print(model.get_double_num(10))
