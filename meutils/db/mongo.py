#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : mimongo
# @Time         : 2020-03-20 11:26
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  :
# https://www.jb51.net/article/159652.htm
# https://www.cnblogs.com/kaituorensheng/p/5181410.html

from meutils.pipe import *
from meutils.decorators import singleton
from pymongo import MongoClient, ReadPreference


class DBConf(BaseConfig):
    database: str
    user: str
    passwd: str
    ips: str
    dns: str
    replicaSet: str


@singleton
class Mongo(object):

    def __init__(self, db='mig3_algo_push', url="mongodb://localhost:27017", only_read=True):
        """
        :param db:
        :param print_info:
        """
        if url is None:
            conf = DBConf.parse_zk('/push/db/mongodb')
            url = f"mongodb://{conf.user}:{conf.passwd}@{conf.dns}/{conf.database}?replicaSet={conf.replicaSet}&authSource=admin"

        self.client = MongoClient(url)
        if only_read:
            self.db = self.client.get_database(db, read_preference=ReadPreference.SECONDARY_PREFERRED)
        else:
            self.db = self.client[db]

        self.client.get_database()

        self.client_info = {
            "主节点": self.client.is_primary,
            "最大连接数": self.client.max_pool_size,
            'self.client.admin.command': self.client.admin.command('ismaster')
        }

    def starter(self):
        """
        # info
        collection.count_documents({})

        # 增
        collection.insert_one({'x': 1})
        collection.insert_one({'xx': 2})
        ids = collection.insert_many([{'xxx': 3}, {'xxx': 4}])

        from bson.objectid import ObjectId

        collection.find_one({'x': 1})
        collection.find_one({'_id': ObjectId('5e743cea06be472ac7298def')})

        # 复杂的查询
        list(collection.find({})) # collection.find().count()
        list(collection.find({'xx': {'$gt': 1}}))

        condition = {'s': 1}
        # update_one update_many
        # result = collection.replace_one(condition, {'s': 1, 'ss': 2}) # 完全替换 # upsert=True强拆
        result = collection.replace_one(condition, {'$set': {'s':1, 'sss': 3}}) # {**d1, **d2}
        """
        pass


if __name__ == '__main__':
    Mongo()
