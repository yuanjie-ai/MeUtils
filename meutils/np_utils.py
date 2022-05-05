#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : np_utils
# @Time         : 2020/11/12 11:35 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 


import numpy as np

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
