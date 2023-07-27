#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : ann_v1
# @Time         : 2021/4/17 12:22 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : pymilvus==1.0.1
import copy
from meutils.pipe import *
from milvus import Milvus, MetricType, IndexType


class ANN(object):

    def __init__(self, host='HOST', port='19530', pool="SingletonThread"):
        self.host = host
        self.client = Milvus(
            host, port,
            handler='GRPC' if port == '19530' else 'HTTP',  # 19530, 19121
            pool=pool,  # 线程池
            pool_size=32,
        )
        logger.info(f"ServerVersion {self.client.server_version()}")
        logger.info(f"ClientVersion {self.client.client_version()}")

    def __getattr__(self, collection_name) -> Collection:
        return Collection(collection_name, self.client)

    def create_collection(self, collection_name='TEST',
                          dim=768,
                          index_file_size=1024,
                          metric_type='IP',
                          index_type='IVF_FLAT',
                          nlist=4096,  # 4*n**0.5
                          partitions=None,
                          auto_id=True,
                          overwrite=True,
                          sleep=6):

        if self.client.has_collection(collection_name):
            if overwrite:
                logger.warning(f"{collection_name} already exists! to drop.")
                self.client.drop_collection(collection_name, timeout=300)
                time.sleep(sleep)  # "Collection already exists and it is in delete state, please wait a second"
            else:
                return f"{collection_name} already exists!"

        # 建表
        params = {
            'collection_name': collection_name,
            'dimension': dim,
            'metric_type': MetricType.__getattr__(metric_type),
            'index_type': IndexType.__getattr__(index_type),
            'index_file_size': index_file_size,
            'index_param': {'nlist': nlist},
            'auto_id': auto_id
        }

        self.client.create_collection(params)
        self.client.create_index(collection_name, params['index_type'], params['index_param'])

        # 分区：删除分区就不需要重新建表
        if partitions is not None:
            for part in partitions:
                self.client.create_partition(collection_name, partition_tag=part)

        logger.info(f"{self.client.get_collection_info(collection_name)}")


class Collection(object):

    def __init__(self, name=None, client=None):
        self.name = name
        self.client = client

    def __str__(self):
        _, ok = self.client.has_collection(self.name)
        if not ok:
            logger.warning(f"{self.name}  doesn't exist")
        return f"Collection({self.name})"

    def insert(self, vectors, batch_size=100000, partition_tag=None):
        # todo: 多进程插入
        ids = []
        n = max(len(vectors) // batch_size, 1)

        for a in tqdm(np.array_split(vectors, n)):
            _, _ids = self.client.insert(self.name, a, partition_tag=partition_tag)
            ids += _ids

        return ids

    def search(self, vectors, topk=10, nprobe=64, partition_tags=None, threshold=None, union=True):
        status, results = self.client.search(
            self.name, topk, vectors,
            partition_tags=partition_tags,
            params={"nprobe": nprobe},
        )

        if threshold:
            dfs = [pd.DataFrame(map(lambda x: x.__dict__, r))[lambda df: df.distance > threshold] for r in results]
        else:
            dfs = [pd.DataFrame(map(lambda x: x.__dict__, r)) for r in results]

        if dfs:
            return pd.concat(dfs) if union else dfs  # id, distance
        else:
            return pd.DataFrame(columns=['id', 'distance'])

    def create_partition(self, partition_tag):
        return self.client.drop_partition(self.name, partition_tag)

    def drop_partition(self, partition_tag):
        return self.client.drop_partition(self.name, partition_tag)

    def get_entity_by_id(self, ids):
        return self.client.get_entity_by_id(self.name, ids)

    def delete_entity_by_id(self, ids):
        return self.client.delete_entity_by_id(self.name, ids)

    @property
    def count(self):
        return self.client.count_entities(self.name)

    @property
    def info(self):
        return self.client.get_collection_info(self.name)[1]

    @property
    def stats(self):
        return self.client.get_collection_stats(self.name)[1]

    @property
    def partitions(self):
        return self.client.list_partitions(self.name)
