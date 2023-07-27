#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : np_utils
# @Time         : 2020/11/12 11:35 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

from itertools import combinations
from collections import defaultdict
# ME
from meutils.pipe import *

# 分组
# np.array_split(range(6), 3)
# iteration_utilities.split
# iteration_utilities.grouper([1,2,3,4], 2) | xlist


# 展平
"""
l=[[1,2,3],[4,[5],[6,7]],[8,[9,[10]]]]*1000
from iteration_utilities import deepflatten
_ = list(deepflatten(l)) # 快十倍
_ = sum(l, [])
"""


def normalize(x):
    if len(x.shape) > 1:
        return x / np.clip(x ** 2, 1e-12, None).sum(axis=1).reshape((-1, 1) + x.shape[2:]) ** 0.5
    else:
        return x / np.clip(x ** 2, 1e-12, None).sum() ** 0.5


def cosine(v1, v2):  # 相似度不是距离
    """
    v1 = np.array([[1, 2], [3, 4]])
    v2 = np.array([[5, 6], [7, 8], [5, 6]])
    cosine_dist(v1, v2)
    """
    assert v1.ndim == v2.ndim
    if v1.ndim == 1:
        v1, v2 = v1.reshape(1, -1), v2.reshape(1, -1)

    from sklearn.metrics.pairwise import cosine_similarity
    return cosine_similarity(v1, v2).clip(0, 1)


def cosine_topk(v1, v2, topk=10):  # 相似度不是距离
    dist = - cosine(v1, v2)
    idxs = np.argsort(dist)[:, :topk]
    scores = - np.take_along_axis(dist, idxs, -1)  # 取出得分
    return idxs[0], scores[0]


def cooccurrence_matrix(texts, window_size=2):
    """
    构建共现矩阵
    :param texts: 文本列表
    :param window_size: 单词之间的最大距离
    :return: 共现矩阵

        data_list = [
                ['I' ,'like','learning', 'like'],
                ['I' ,'like','playing'],
            ]
        print(cooccurrence_matrix(data_list, 4))
    """
    # 统计单词出现的次数
    word_counts = defaultdict(int)
    for text in texts:
        for word in text:
            word_counts[word] += 1

    # 创建单词-id映射
    word_to_id = {word: i for i, word in enumerate(word_counts)}
    i2w = {i: w for w, i in word_to_id.items()}

    # 初始化共现矩阵
    matrix = np.zeros((len(word_counts), len(word_counts)))

    # 统计共现次数
    for text in tqdm(texts):
        for i, j in combinations(range(len(text)), 2):
            if abs(i - j) <= window_size:
                word_i, word_j = text[i], text[j]
                if word_i in word_to_id and word_j in word_to_id:
                    matrix[word_to_id[word_i], word_to_id[word_j]] += 1
                    matrix[word_to_id[word_j], word_to_id[word_i]] += 1
    index = list(i2w.values())
    columns = list(i2w.values())
    return pd.DataFrame(matrix, index, columns)


if __name__ == "__main__":
    import time
    from sklearn.metrics.pairwise import cosine_similarity

    x = np.random.rand(10, 128)
    y = np.random.rand(1000000, 128)
    idxs, scores = cosine_topk(x[:1], x)
    print(idxs[0])
