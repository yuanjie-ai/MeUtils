#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : cache_utils
# @Time         : 2021/11/24 上午11:09
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://cachetools.readthedocs.io/en/stable/
"""
FIFO：First In、First Out，就是先进先出。

LFU：Least Frequently Used，就是淘汰最不常用的。

LRU：Least Recently Used，就是淘汰最久不用的。

MRU：Most Recently Used，与 LRU 相反，淘汰最近用的。

RR：Random Replacement，就是随机替换。

TTL：time-to-live 的简称，也就是说，Cache 中的每个元素都是有过期时间的，如果超过了这个时间，那这个元素就会被自动销毁。
如果都没过期并且 Cache 已经满了的话，那就会采用 LRU 置换算法来替换掉最久不用的，以此来保证数量。
"""
import pickle
from joblib import Memory
from loguru import logger
from cachetools import cached, cachedmethod, LRUCache, RRCache, TTLCache
from meutils.decorators.decorator import decorator
from functools import lru_cache

def map_cache():
    return cached({})


def ttl_cache(ttl=60, maxsize=1024):
    """https://cachetools.readthedocs.io/en/stable/

        @ttl_cache()
        @disk_cache()
        def reader():  # 多级缓存

            time.sleep(1)
    """
    return cached(TTLCache(maxsize, ttl))  # LRUCache


@decorator
def redis_cache(func, rc=None, ex=3, *args, **kwargs):
    """redis 缓存"""
    k = f"cache:{func.__name__}"

    if k in rc:
        return pickle.loads(rc.get(k))
    else:
        logger.info(f"CacheKey: {k}")
        _ = func(*args, **kwargs)
        rc.set(k, pickle.dumps(_), ex=ex)
        return _


@decorator
def disk_cache(func, location='cachedir', *args, **kwargs):
    """硬盘缓存"""
    memory = Memory(location=location)
    return memory.cache(func)(*args, **kwargs)
