#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : DataType
# @Time         : 2020/12/9 6:20 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 


from enum import IntEnum


class DataType(IntEnum):
    NULL = 0
    INT8 = 1
    INT16 = 2
    INT32 = 3
    INT64 = 4

    STRING = 20

    BOOL = 30

    FLOAT = 40
    DOUBLE = 41

    VECTOR = 100
    UNKNOWN = 9999
