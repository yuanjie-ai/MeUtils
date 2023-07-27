#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : dist_utils
# @Time         : 2020/12/9 3:13 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm https://github.com/yuanjie-ai/DNN/blob/master/8_NLP/0_utils/Levenshtein.md
# @Description  : 几何距离、编辑距离、语义距离等
"""

Levenshtein.distance(str1, str2) # 描述由一个字串转化成另一个字串最少的操作次数，在其中的操作包括插入、删除、替换。算法实现：动态规划
Levenshtein.hamming(str1, str2) # 要求str1和str2必须长度一致。是描述两个等长字串之间对应位置上不同字符的个数
Levenshtein.ratio(str1, str2) # r=(sum–ldist)/sum, sum=len(str1)+len(str2),ldist是类编辑距离。在类编辑距离中删除、插入依然+1，但是替换+2
Levenshtein.jaro(str1, str2) # Jaro Distance # 据说是用来判定健康记录上两个名字是否相同，也有说是是用于人口普查
Levenshtein.jaro_winkler(str1, str2) # 给予了起始部分就相同的字符串更高的分数

Levenshtein.seqratio(['newspaper', 'litter bin', 'tinny', 'antelope'], ['caribou', 'sausage', 'gorn', 'woody']) # like ratio()
Levenshtein.setratio(['newspaper', 'litter bin', 'tinny', 'antelope'], ['caribou', 'sausage', 'gorn', 'woody'])

"""

from sklearn.metrics.pairwise import cosine_similarity

# ME
from meutils.pipe import *


def jaccard(a, b):
    a, b = map(set, (a, b))
    return 1 - len(a & b) / len(a | b)


def get_sorted_top_k(array, top_k=1, axis=-1, reverse=False):  # 不准
    """https://blog.csdn.net/danengbinggan33/article/details/112525700
    多维数组排序
    Args:
        array: 多维数组
        top_k: 取数
        axis: 轴维度
        reverse: 是否倒序

    Returns:
        top_sorted_scores: 值
        top_sorted_indexes: 位置
    """
    if reverse:
        # argpartition分区排序，在给定轴上找到最小的值对应的idx，partition同理找对应的值
        # kth表示在前的较小值的个数，带来的问题是排序后的结果两个分区间是仍然是无序的
        # kth绝对值越小，分区排序效果越明显
        axis_length = array.shape[axis]
        partition_index = np.take(np.argpartition(array, kth=-top_k, axis=axis),
                                  range(axis_length - top_k, axis_length), axis)
    else:
        partition_index = np.take(np.argpartition(array, kth=top_k, axis=axis), range(0, top_k), axis)
    top_scores = np.take_along_axis(array, partition_index, axis)
    # 分区后重新排序
    sorted_index = np.argsort(top_scores, axis=axis)
    if reverse:
        sorted_index = np.flip(sorted_index, axis=axis)
    top_sorted_scores = np.take_along_axis(top_scores, sorted_index, axis)
    top_sorted_indexes = np.take_along_axis(partition_index, sorted_index, axis)
    return top_sorted_scores, top_sorted_indexes


# simhash https://blog.csdn.net/Trisyp/article/details/113623966

if __name__ == "__main__":
    import time
    from sklearn.metrics.pairwise import cosine_similarity

    x = np.random.rand(10, 128)
    y = np.random.rand(1000000, 128)

    start_time = time.time()
    z = cosine_similarity(x, y)
    sorted_index_1 = get_sorted_top_k(z, top_k=3, axis=1, reverse=True)[1]
    print(time.time() - start_time)

    start_time = time.time()
    z = cosine_similarity(x, y)
    sorted_index_2 = np.flip(np.argsort(z, axis=1)[:, -3:], axis=1)
    print(time.time() - start_time)

    print((sorted_index_1 == sorted_index_2).all())
    print(get_sorted_top_k(z, top_k=3, axis=1, reverse=True))
