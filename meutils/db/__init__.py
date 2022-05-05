#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : __init__.py
# @Time         : 2020/11/26 2:57 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  :
from meutils.pipe import *


class DB(object):

    def __init__(self, is_test=None):

        if is_test is None:
            if HOST_NAME.__contains__('local') or LOCAL:
                is_test = True

        self.is_test = is_test

    def redis(self, ips=None, password=None, batch=False):  # redis集群
        """
        # todo: 批量插入（[(k, v),]）or yield
        @param ips:
        @param password:
        @param batch:
        @return:
        """
        if self.is_test:
            return {}

        from rediscluster import RedisCluster  # pip install redis-py-cluster

        startup_nodes = [dict(zip(['host', 'port'], ip.split(':'))) for ip in ips]

        rc = RedisCluster(
            startup_nodes=startup_nodes,
            decode_responses=True,
            skip_full_coverage_check=True,
            password=password,
        )
        if batch:
            return rc.pipeline()  # DB().redis.execute()

        else:
            return rc

    def mysql(self, host='29.69.112.01'[::-1], port=3306, user='db_ai', passwd='db_Ai2019', db='ai'):
        import pymysql
        return pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)

    def mongodb(self):
        pass

    def hive(self):
        pass


class Redis(object):
    """
    rc.delete
    rc.lpush('lpush', 'a', 'b') # ['b', 'a']
    rc.rpush('rpush', 'a', 'b') # ['a', 'b']
    rc.lrange('rpush', 0, 10)
    rc.lrange('lpush', 0, 10)

    rc.hmset('hmset', {'a': 1, 'b': 2})
    rc.hmget('hmset', 'a')

    rc.sadd('sadd', 0)
    rc.smembers('sadd')

    rc.zadd('zadd', mapping={'a': 888, 'b': 1})
    rc.zrange('zadd', 0, 1000, desc=True)
    """

    def __init__(self, ips=None, password=None, decode_responses=False):

        if isinstance(ips, str):
            import redis

            self.rc = redis.Redis(
                *ips.split(':'),
                password=password,
                decode_responses=decode_responses
            )

        else:
            from rediscluster import RedisCluster

            startup_nodes = [dict(zip(['host', 'port'], ip.split(':'))) for ip in ips]

            self.rc = RedisCluster(
                startup_nodes=startup_nodes,
                password=password,
                decode_responses=decode_responses,  # get对象设置False decode
                skip_full_coverage_check=True,
            )
        self.rc.set_obj = self._set_obj
        self.rc.get_obj = self._get_obj

        self.rc.setobject = self._set_obj
        self.rc.getobject = self._get_obj

    @timer("RedisInsertData")
    def insert(self, values, insert_fn=lambda k, v, p: p.set(k, v)):
        with self.rc.pipeline(transaction=False) as p:  # 事务：原子性、一致性、隔离性、持久性

            _insert_fn = functools.partial(insert_fn, p=p)
            for v in tqdm(values):  # xJobs
                _insert_fn(*v)

            p.execute()

    def _set_obj(self, key, obj, ex=None, px=None, nx=False, xx=False, keepttl=False):
        self.rc.set(key, pickle.dumps(obj), ex, px, nx, xx, keepttl)

    def _get_obj(self, key, default=None):
        try:
            _ = self.rc.get(key)
            return pickle.loads(_) if _ else default

        except Exception as e:
            print(e)


if __name__ == '__main__':
    rc = Redis('9736:071.4.9.931'[::-1], password='*', decode_responses=True).rc

    rc.set('a', 'xxxx')

    print(rc.get('a'))
