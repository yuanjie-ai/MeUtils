#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : demo
# @Time         : 2020-02-14 11:52
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  :
# https://github.com/milvus-io/docs/blob/master/site/en/guides/milvus_operation.md#createdrop-indexes-in-a-collection
# https://github.com/milvus-io/pymilvus/tree/master/examples/indexes
# https://raw.githubusercontent.com/milvus-io/pymilvus/0.7.0/examples/example.py
# TODO:
# m.milvus.preload_table

from meutils.pipe import *
from milvus import Milvus, DataType
import copy

# IndexType.

# from milvus.client.exceptions import CollectionNotExistException

"""
client.drop_index
client.get_config
client.list_id_in_segment
client.load_collection???
"""


class Collection(object):

    def __init__(self, name=None, client=None):
        self.name = name
        self.client = client
        self.count_entities = self.count
        self.count_documents = self.count
        self.vector_name = self.get_vec_field_name()

    def __str__(self):
        has_collection = self.client.has_collection(self.name)
        if not has_collection:
            logger.warning(f"{self.name}  doesn't exist")
        return f"Collection({self.name})"

    def batch_insert(self, df_entity: pd.DataFrame, batch_size=100000):
        """

        :param df_entity: id, sid, vec, part 与 collection 字段一致
        :param batch_size:
        :return:
        """
        entity_names = [_['name'] for _ in self.collection_info['fields']]
        logger.warning(f"EntityNames: {entity_names}")

        # 分区
        df_entity = df_entity.reset_index(drop=True)
        n = len(df_entity)
        num_part = n // batch_size + 1 if n % batch_size else n // batch_size

        ids = []
        for i in tqdm(range(num_part), desc='BatchInsert'):
            df = df_entity.iloc[i * batch_size:(i + 1) * batch_size, :]
            entities = []
            for record in self.collection_info['fields']:
                entities.append({
                    'name': record['name'],
                    'type': record['type'],
                    'values': df[record['name']].values
                })

            ids += self.client.insert(self.name, entities, ids=df['id'] if 'id' in df else None)
            time.sleep(3)
        return ids

    def search(
            self, vectors=np.random.random((1, 256)),
            topk=10,
            nprobe=1,
            scalar_list: List[dict] = None):
        q = self.get_search_query(vectors, topk, nprobe, scalar_list)
        entities = self.client.search(self.name, q)[0]

        return entities  # todo: 增加阈值过滤

        # entities = ann.client.search("demo", query_hybrid)[0]
        # id2score = dict(zip(entities.ids, entities.distances))

        # docs = mongo_collection.find({"xindaoid": {'$in': entities.ids}})
        # df = pd.DataFrame(list(docs)).drop(['_id', 'category_', 'vector'], 1)
        # df['distance'] = df['xindaoid'].map(id2score)

    def batch_search(self, vectors=np.random.random((1, 256)), topk=10, nprobe=1,
                     scalar_list: List[dict] = None):
        q = self.get_search_query(vectors, topk, nprobe, scalar_list)
        entities = self.client.search(self.name, q)
        return entities

    def get_entity_by_id(self, ids, fields=None):
        return self.client.get_entity_by_id(self.name, ids, fields)

    def delete_entity_by_id(self, ids):
        self.client.delete_entity_by_id(self.name, ids)

    @property
    def count(self):
        return self.client.count_entities(self.name)

    @property
    def collection_info(self):
        return self.client.get_collection_info(self.name)

    @property
    def collection_stats(self):
        return self.client.get_collection_stats(self.name)

    def get_vec_field_name(self):
        fields = self.collection_info['fields']
        vec_field = [_ for _ in fields if str(_.get('type', '')).__contains__('VECTOR')][0]
        return vec_field['name']

    def get_search_query(self, vectors, topk=10, nprobe=1, scalar_list: List[dict] = None):
        """
        ann.demo.search(np.random.random((1, 10)), scalar_list=[{'term': {'scalar': [1,2,3,4]}}])
        :param vectors:
        :param topk:
        :param nprobe:
        :param scalar_list:
        :return:
        """
        q = {
            "bool": {
                "must": [
                    {
                        "vector": {
                            self.vector_name: {
                                "topk": topk,
                                "query": vectors,
                                "metric_type": "IP",
                                "params": {
                                    "nprobe": nprobe
                                }
                            }
                        }
                    },
                ]
            }
        }
        if scalar_list is not None:  # {"term": {"标量字段": [1,2,3]}}
            for _ in scalar_list:
                q['bool']['must'].append(_)
        return q


class ANN(object):

    def __init__(self, host='HOST', port='19530', handler="GRPC", pool="SingletonThread", show_info=False):
        self.host = host
        self.client = Milvus(host, port, handler=handler, pool=pool, pool_size=32)  # 线程池

        if show_info:
            logger.info(
                {
                    "ClientVersion": self.client.client_version(),
                    "ServerVersion": self.client.server_version()
                }
            )

    def __getattr__(self, collection_name) -> Collection:
        return Collection(collection_name, self.client)

    def create_collection(self, collection_name, fields, auto_id=True, segment_row_limit=4096, overwrite=True):
        """

        :param collection_name:
        :param fields: # type: BOOL INT32 INT64 FLOAT BINARY_VECTOR FLOAT_VECTOR
            fields = [
                {
                    "name": "scalar",
                    "type": 'INT32',
                    "params": {},
                    "indexes": [{}]
                },
                {
                    "name": "vector",
                    "type": 'FLOAT_VECTOR',
                    "params": {"dim": 768},
                    "indexes": [{"index_type": 'IVF_FLAT', 'metric_type': 'IP', 'params': {'nlist': 1024}, 'index_file_size': 1024}]
                }
            ]
        # index_file_size不确定放在哪生效
        :param auto_id:
        :param segment_row_limit: range 4096 ~ 4194304
        :return:
        """
        fields = copy.deepcopy(fields)  # fields[:]

        if self.client.has_collection(collection_name):
            if overwrite:
                logger.warning(f"{collection_name} already exists! to drop.")
                self.client.drop_collection(collection_name, timeout=300)
            else:
                return f"{collection_name} already exists!"

        vec_field = [_ for _ in fields if _.get('type', '').__contains__('VECTOR')][0]
        # assert len(vec_fields) > 0, "至少有一个矢量"

        for _ in fields:
            if 'type' in _:
                _['type'] = DataType.__getattr__(_['type'])

        collection_param = {
            "fields": fields,
            "auto_id": auto_id,
            "segment_row_limit": segment_row_limit,
        }

        # collection vector index
        self.client.create_collection(collection_name, fields=collection_param)

        self.client.create_index(collection_name, vec_field['name'], vec_field['indexes'][0])

        logger.info(f"{self.client.get_collection_info(collection_name)}")

    @property
    def collection_names(self):
        return self.client.list_collections()

    def __create_index(self, collection_name, field_name, index_type='IVF_FLAT', metric_type='IP', index_params=None):

        if index_params is None:
            index_params = {'nlist': 1024}

        params = {
            'index_type': index_type,
            # 'index_file_size': 1024, # TODO: 不确定放在哪生效
            'params': index_params,

            'metric_type': metric_type,
        }
        self.client.create_index(collection_name, field_name, params)  # field_name='embedding'


if __name__ == '__main__':
    ann = ANN('HOST', show_info=True)
    fields = [
        {
            "name": "scalar",
            "type": 'INT32',
            "params": {},
            "indexes": [{}]
        },
        {
            "name": "vector",
            "type": 'FLOAT_VECTOR',
            "params": {"dim": 256},
            "indexes": [
                {"index_type": 'IVF_FLAT', 'metric_type': 'IP', 'params': {'nlist': 1024}, 'index_file_size': 1024}]
        }
    ]
    ann.create_collection('demo', fields)
    print(ann.demo)
    print(ann.demo.collection_info)
    print(ann.demo.vector_name)
    # print(ann.demo.collection_stats)

    # df列名必须与fields一致
    df = pd.DataFrame(enumerate('abcdefgh'), columns=['scalar', 'sid']).assign(
        vector=np.random.random((8, 256)).tolist())

    ann.demo.batch_insert(df)
