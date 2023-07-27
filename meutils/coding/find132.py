#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : find132
# @Time         : 2021/3/24 4:20 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 
from typing import *

class Solution:
    def find132pattern(self, nums: List[int]) -> bool:


        n = len(nums)
        candidate_k = [nums[n - 1]]
        max_k = float("-inf")

        for i in range(n - 2, -1, -1):
            if nums[i] < max_k:
                return True
            while candidate_k and nums[i] > candidate_k[-1]:
                max_k = candidate_k[-1]
                candidate_k.pop()
            if nums[i] > max_k:
                candidate_k.append(nums[i])

        return False


# import bisect
#
# a = [1, 4, 6, 8, 12, 15, 20]
# position = bisect.bisect(a, 13)
# print(position)
#
# # 用可变序列内置的insert方法插入
# a.insert(position, 13)
# print(a)
