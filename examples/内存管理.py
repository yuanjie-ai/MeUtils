#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : 内存管理
# @Time         : 2021/3/10 6:11 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from memory_profiler import profile


@profile
def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a


from meutils.pipe import *
from meutils.pd_utils import df_split

df = pd.DataFrame(np.random.random((10000, 10000)))


@profile
def df_func(df):

    for df_ in df_split(df, 20):
        vecs = [[12345] * 100] * len(df_)

        df_['vector'] = vecs
    df = None
    # del df



"""
del 有用
函数结尾相当于操作gc.collect()
"""
if __name__ == '__main__':
    df_func(df)
    print(df.head())
