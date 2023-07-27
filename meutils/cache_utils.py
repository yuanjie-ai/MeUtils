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
异步缓存 from aiocache import cached

FIFO：First In、First Out，就是先进先出。

LFU：Least Frequently Used，就是淘汰最不常用的。

LRU：Least Recently Used，就是淘汰最久不用的。

MRU：Most Recently Used，与 LRU 相反，淘汰最近用的。

RR：Random Replacement，就是随机替换。

TTL：time-to-live 的简称，也就是说，Cache 中的每个元素都是有过期时间的，如果超过了这个时间，那这个元素就会被自动销毁。
如果都没过期并且 Cache 已经满了的话，那就会采用 LRU 置换算法来替换掉最久不用的，以此来保证数量。
"""
import sys
import math
import pickle
import hashlib
import numpy as np
import pandas as pd
import inspect
import joblib

from typing import Iterable
from functools import lru_cache
from pathlib import Path
from joblib import Memory
from joblib.func_inspect import filter_args
from joblib import hashing  # hashing.hash

from loguru import logger
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from tqdm.auto import tqdm
from cachetools import cached, cachedmethod, LRUCache, RRCache, TTLCache as _TTLCache, keys

# ME
from meutils.decorators import decorator, singleton, background_task
from meutils.hash_utils import md5

TTLCache = lru_cache()(_TTLCache)


def map_cache():
    return cached({})


def ttl_cache(ttl=60, maxsize=1024, key=keys.hashkey):
    """https://cachetools.readthedocs.io/en/stable/

        @ttl_cache()
        @disk_cache()
        def fn(x):  # 多级缓存
            time.sleep(1)
            return x

    @param ttl:
    @param maxsize:
    @param key: key_fn = lambda *args, **kwargs: f"{args}{kwargs}" # todo: 长数组支持有问题
    @return:
    """

    return cached(TTLCache(maxsize, ttl), key=key)  # LRUCache


@decorator
def redis_cache(func, rc=None, ex=3, *args, **kwargs):
    """redis 缓存"""
    k = f"cache_{func.__name__}_{args}_{kwargs}"

    if k in rc:
        return pickle.loads(rc.get(k))
    else:
        logger.info(f"CacheKey: {k}")
        _ = func(*args, **kwargs)
        rc.set(k, pickle.dumps(_), ex=ex)
        return _


@decorator
def cache4df(func, db='cache.db', verbose=1, *args, **kwargs):
    """返回值是df"""
    import sqlite3
    conn = sqlite3.connect(db)
    tables = set(pd.read_sql(f'select * from sqlite_master', conn)['tbl_name'])

    k = f"cache_{func.__name__}_{args}_{kwargs}"
    if k in tables:
        return pd.read_sql(f'select * from `{k}`', conn)
    else:
        if verbose:
            logger.info(f"CacheKey: {k}")

        df = func(*args, **kwargs)
        df.to_sql(k, conn, if_exists='replace', index=False)
        return df


@decorator
def diskcache(func, location='cachedir', ttl=None, ignore=None, verbose=1, tag=None, *args, **kwargs):
    """
    https://zhuanlan.zhihu.com/p/356447502
    https://grantjenks.com/docs/diskcache/

    """
    from diskcache import Cache, FanoutCache

    cache = Cache(directory=location)

    raw_key = dict(filter_args(func, [], list(args), kwargs))
    raw_key = {**raw_key.pop('**', {}), **raw_key, '__tag__': tag or func.__name__}

    # self cls 看场景选择
    ignore = (ignore or []) + [
        'api_base', 'api_key', 'openai_api_base', 'openai_api_key',
        'organization', 'openai_organization',
        'request_timeout'
    ]

    for arg in ignore:
        raw_key.pop(arg, None)

    key = hashing.hash(raw_key)

    _ = cache.get(key, '__in__')
    if _ == '__in__':
        _ = func(*args, **kwargs)
        if inspect.isgenerator(_):
            _ = list(_)
            cache.set(f"{key}_isgenerator", True, expire=ttl)

        cache.set(key, _, expire=ttl)  # 异步写入

        if verbose:
            from loguru import logger
            logger = logger.patch(lambda r: r.update(name=func.__name__))
            logger.info(f"{cache.directory}: `CacheKey: {raw_key if verbose != 1 else key}`")

    return _ if not cache.get(f"{key}_isgenerator") else iter(_)


@decorator
def disk_cache(func, location='cachedir', maxsize=128, ttl=np.inf, verbose=True, *args, **kwargs):
    ttl_cache = TTLCache(maxsize, ttl)  # 单例

    k = md5(f"cache_{func.__name__}_{args}_{kwargs}")  # uuid
    output = Path(location) / Path(k) / '__output.pkl'

    if (ttl == np.inf or k in ttl_cache) and output.is_file():  # ttl=np.inf 不作key判断, 相当于maxsize无穷大
        # return joblib.load(output)
        return pickle.load(open(output, 'rb'))

    else:

        _ = func(*args, **kwargs)

        @background_task
        def dump():
            if verbose: logger.info(f"CacheKey: {k}")

            output.parent.mkdir(parents=True, exist_ok=True)
            pickle.dump(_, open(output, 'wb'))
            ttl_cache[k] = 0  # 更新cache

        dump()
        return _


@decorator
def joblib_cache(func, location='cachedir', ignore=None, compress=False, verbose=1, *args, **kwargs):
    """硬盘缓存

    @param func:
    @param location:
    @param ignore: 有时我们不希望因某些参数的改变而导致重新计算，例如调试标志。
        @memory.cache(ignore=['debug'])
        def my_func(x, debug=True):
            print('Called with x = %s' % x)
    @param compress:
    @param verbose:
    @param args:
    @param kwargs:
    @return:
    """
    memory = Memory(location=location, verbose=verbose, compress=compress)
    return memory.cache(func, ignore)(*args, **kwargs)


@decorator
def cache4batch(func, location='cachedir', verbose=1, *args, **kwargs):
    """disk_cache 存中存

        @disk_cache()
        def f(x):
            return x

        [1,2,3] | xmap_(f)

    @param func: 单条入参（转batch)
    @param location:
    @param verbose:
    @param args:
    @param kwargs:
    @return: 由单条输入转为可多条输入  # TODO 放弃，违背装饰器原则，改变了输入输出
    """

    @disk_cache(location=location)
    def wrap(batch):
        if isinstance(batch, Iterable) and not isinstance(batch, str):
            if verbose:
                batch = tqdm(batch, desc='miss')
            return list(map(wrap, batch))  # 递归
        return func(batch)  # 需支持单条输入

    return wrap(args[0])


class MomentoCache(object):

    def __init__(self, cache_name='TEST', ttl=24 * 3600):
        from datetime import timedelta

        from momento import CacheClient, Configurations, CredentialProvider

        self.cache_name = cache_name
        self.cache_client = CacheClient(
            configuration=Configurations.Laptop.v1(),
            credential_provider=CredentialProvider.from_environment_variable('MOMENTO_AUTH_TOKEN'),
            default_ttl=timedelta(seconds=ttl)
        )
        self.cache_client.create_cache(self.cache_name)

    def set(self, key, value, expire=None):
        try:
            self.cache_client.set(self.cache_name, key, pickle.dumps(value))
            return True
        except Exception as e:
            logger.error(e)
            return False

    def get(self, key, default=None):
        from momento.responses import CacheGet, CacheSet, CreateCache

        get_response = self.cache_client.get(self.cache_name, key)
        if isinstance(get_response, CacheGet.Hit):
            return pickle.loads(get_response.value_bytes)
        return default


@decorator
def cache(func, cache_name='cachedir', ttl=None, ignore=None, verbose=1, tag=None, *args, **kwargs):
    cache = MomentoCache(cache_name)  # 缓存类

    raw_key = dict(filter_args(func, [], list(args), kwargs))

    ignore = (ignore or []) + ['self', 'cls', 'api_base', 'api_key', 'organization', 'request_timeout']  # self 本身就不被计入
    raw_key = {**raw_key.pop('**', {}), **raw_key, '__tag__': tag or func.__name__}
    for arg in ignore:
        raw_key.pop(arg, None)

    key = hashing.hash(raw_key)

    _ = cache.get(key)
    if _ is None:
        _ = func(*args, **kwargs)
        if inspect.isgenerator(_):
            _ = list(_)
            cache.set(f"{key}_isgenerator", True, expire=ttl)

        cache.set(key, _, expire=ttl)  # 异步写入

        if verbose:
            from loguru import logger
            logger = logger.patch(lambda r: r.update(name=func.__name__))
            logger.info(f"{cache.cache_name}: `CacheKey: {raw_key if verbose != 1 else key}`")

    return _ if not cache.get(f"{key}_isgenerator") else iter(_)


if __name__ == '__main__':
    from meutils.pipe import *
