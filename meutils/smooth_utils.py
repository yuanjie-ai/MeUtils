#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : smooth_utils
# @Time         : 2021/3/18 12:27 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 平滑函数

from meutils.pipe import *

"""
TODO: 增加可视化
"""


def exponential_decay(t, life_cycle=24 * 7, start=1, end=0):
    """牛顿冷却定律
    拟合随时间指数衰减的过程
    https://blog.csdn.net/xiaokang06/article/details/78076925
    https://blog.csdn.net/zhufenghao/article/details/80879260

    其中α为衰减常数，通过回归可计算得出。例如：指定45分钟后物体温度为初始温度的0.5，即 0.5=1×exp(-a×45)，求得α=0.1556。

    :param t: 0~delta
    :param life_cycle: 衰减时间长度/生命周期
    :param start: 起始值
    :param end: 结束值
    :return:
    """

    α = np.log(start / (end + 1e-8)) / life_cycle
    t0 = - np.log(start) / α

    decay = np.exp(- α * (t + t0))
    return decay


def walson_ctr(num_click, num_pv, z=1.96):
    """:arg
    威尔逊
    https://mp.weixin.qq.com/s/rLP1wsS0a71q5RA7NQcjdQ
    """
    p = num_click / num_pv
    if p > 0.9:
        return 0.0

    n = num_pv

    A = p + z ** 2 / (2 * n)
    B = np.sqrt(p * (1 - p) / n + z ** 2 / (4 * (n ** 2)))
    C = z * B

    D = 1 + z ** 2 / n

    ctr = (A - C) / D

    return ctr
