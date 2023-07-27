#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : hot_update
# @Time         : 2020/12/3 9:31 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : https://www.jianshu.com/p/2d31f1c7ef63

import time
from kazoo.retry import KazooRetry

from kazoo.client import KazooClient

# def func():
#
#     print(time.time())
#     with open('./config.txt') as f:
#         return f.read().strip()
#
# print(KazooRetry()(func))
#
# while 1:
#     time.sleep(2)
#     KazooRetry()(func)

zk = KazooClient(hosts="127.0.0.1:2181")

