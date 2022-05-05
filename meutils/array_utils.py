#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : array_utils
# @Time         : 2021/4/15 3:34 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


def multi_list(ls, n=10):
    return sum(([i] * n for i in ls), [])


if __name__ == '__main__':
    ls = range(5)

    print(multi_list(ls, 3))
