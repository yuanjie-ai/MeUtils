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


def train_valid_test_split(df, test_size=0.3, random_state=None, stratify=None):
    df_train, df_test = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify
    )

    df_valid, df_test = train_test_split(df_test, test_size=0.5, random_state=random_state)  # stratify

    return df_train, df_valid, df_test

from tqdm import tqdm