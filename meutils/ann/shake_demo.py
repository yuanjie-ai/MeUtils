#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : shake_demo
# @Time         : 2021/3/30 4:43 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 在10万召回1万场景下，分10个片区 shake范围在 6.8%【10%以内】


import faiss
from meutils.pipe import *
from meutils.annzoo.faiss import ANN
from meutils.np_utils import normalize

np.random.seed(666)

data = normalize(np.random.random((100000, 128)).astype('float32'))
target = normalize(np.random.random((1, 128)).astype('float32'))

ann = ANN()
ann.train(data, metric=faiss.METRIC_INNER_PRODUCT, index_factory='IVF1,Flat')

N = 10000
dis, idx = ann.search(target, topK=N)
idx_list = []
for i in range(10):
    data_ = data[i * N:(i + 1) * N]
    ann_ = ANN()
    ann_.train(data_, metric=faiss.METRIC_INNER_PRODUCT, index_factory='IVF1,Flat')
    idx_ = ann_.search(target, topK=N // 10)[1] + i * N
    idx_list.append(idx_)

r = set(np.row_stack(idx_list).reshape(1, -1).tolist()[0])
len(set(idx[0].tolist()) - r)
