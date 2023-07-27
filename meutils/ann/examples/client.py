#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-ANN.
# @File         : client
# @Time         : 2020-02-14 15:10
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 


import numpy as np
from milvus import Milvus, IndexType, MetricType

from gensim.models.fasttext import load_facebook_model

fasttext = load_facebook_model('../data/wv/skipgram.title')


def noramlize(x):
    return x / np.linalg.norm(x, 2, axis=len(x.shape) > 1, keepdims=True)


vectors = noramlize(fasttext.wv.vectors).tolist()

id2word = dict(enumerate(fasttext.wv.index2entity))

(np.array(vectors[1471]) * np.array(vectors[13236])).sum()

milvus = Milvus()
milvus.connect(host='HOST', port='19530')

_, ok = milvus.has_table('fasttext')
print(_)
if not ok:
    milvus.create_table(
        param={'table_name': 'fasttext',
               'dimension': 200,
               'index_file_size': 1024,  # optional
               'metric_type': MetricType.IP  # optional
               })

milvus.insert('fasttext', vectors, list(range(len(vectors))))

index_param = {
    'index_type': IndexType.IVFLAT,  # choice ivflat index
    'nlist': 2048
}
milvus.create_index('fasttext', index_param)

param = {
    'table_name': 'fasttext',
    'query_records': [vectors[1471]],
    'top_k': 10,
    'nprobe': 16
}
status, results = milvus.search_vectors(**param)

dict(zip(map(id2word.__getitem__, *results.id_array), *results.distance_array))
