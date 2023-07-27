#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : seize
# @Time         : 2021/2/26 6:51 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : xgb/lgb 参数https://www.jianshu.com/p/1100e333fcab


# import wandb
#
# WANDB_API_KEY = '789ae399af943555652e476ff1d0c0452ee86564'
# wandb.login(key=WANDB_API_KEY)
#
# wandb.init()

from meutils.pipe import *
from xgboost import XGBClassifier
from sklearn.datasets import make_classification


def run(n_estimators=1000000):
    """

    :param n_estimators:
    :return:
    """

    X, y = make_classification(n_estimators)
    clf = XGBClassifier(learning_rate=1 / n_estimators, n_estimators=n_estimators, n_jobs=-1)

    try:
        clf.set_params(tree_method='gpu_hist', predictor='gpu_predictor')
        clf.fit(X, y, eval_set=[(X, y), (X, y)])

    except Exception as e:
        logger.warning(e)
        clf.fit(X, y, eval_set=[(X, y), (X, y)])


if __name__ == '__main__':
    with timer('seize'):
        run(100)
