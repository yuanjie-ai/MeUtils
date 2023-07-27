#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : __init__.py
# @Time         : 2020/10/21 10:41 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

import pandas as pd


def save_sub(df, file, header=False):
    df.to_csv(file, index=False, header=header)
