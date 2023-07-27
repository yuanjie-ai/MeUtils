#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : sk_utils
# @Time         : 2022/4/7 下午1:57
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from sklearn.model_selection import train_test_split

# ME
from meutils.pipe import *


def train_valid_test_split(df, y=None, test_size=0.3, random_state=None):
    if y is None:
        df_train, df_test = train_test_split(df, test_size=test_size, random_state=random_state, stratify=y)
    else:
        df_train, df_test, _, y = train_test_split(df, y, test_size=test_size, random_state=random_state, stratify=y)

    df_val, df_test = train_test_split(df_test, test_size=0.5, random_state=random_state, stratify=y)
    return df_train, df_val, df_test

