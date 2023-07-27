#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-ANN.
# @File         : ANN
# @Time         : 2019-12-04 20:05
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 尽量统一接口
# 从内存
# 从文件
# todo: 增加idmapping并提供在线服务


import gensim


class ANN(object):

    def __init__(self, vector_size=768):
        self.model = gensim.models.KeyedVectors(vector_size)

    def add_vec(self, vectors, ids=None, replace=False):
        """todo 多次加载好像有问题"""
        if ids is None:
            ids = range(len(vectors))
        self.model.add_vectors(ids, vectors, replace=replace)
        # self.model.fill_norms(force=True)  # 归一化
        return self


if __name__ == '__main__':
    import numpy as np

    ann = ANN()
    vectors = np.random.random((10, 768))

    ann.add_vec(vectors)
    _ = ann.model.similar_by_vector(vectors[0])
    print(_)
