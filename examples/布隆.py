#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : 布隆
# @Time         : 2021/4/8 3:40 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://www.cnblogs.com/yscl/p/12003359.html
# https://krisives.github.io/bloom-calculator/
# https://www.cnblogs.com/yscl/p/12003359.html
# 某样东西一定不存在或者可能存在

from pybloom_live import ScalableBloomFilter, BloomFilter

# 可自动扩容的布隆过滤器
bloom = ScalableBloomFilter(initial_capacity=100, error_rate=0.001)

url1 = 'http://www.baidu.com'
url2 = 'http://qq.com'

bloom.add(url1)
print(url1 in bloom)
print(url2 in bloom)
