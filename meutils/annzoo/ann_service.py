#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-ANN.
# @File         : ann_service
# @Time         : 2021/1/31 11:25 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  :

from meutils.zk_utils import *
from appzoo import App
from annzoo.ann import ANN, Collection


# 实时更新配置
@zk.DataWatch('/push/easyann/ann_service')
def watcher(data, stat):  # (data, stat, event)
    ZKConfig.info = yaml.safe_load(data)  # biz2ip



biz2client = {biz: ANN(ip) for biz, ip in ZKConfig.info.items()}


def searcher(**kwargs):
    # DataModel
    biz = kwargs.get('biz')
    collection = kwargs.get('collection')

    topk = kwargs.get('topk', 10)
    nprobe = kwargs.get('nprobe', 1)
    scalar_list = kwargs.get('scalar_list', 1)
    vectors = kwargs.get('vectors', None)

    if vectors is None:
        ids = kwargs.get('ids', None)
        # id mapping
        vectors = ...

    c: Collection = biz2client[biz].__getattr__(collection)
    c.search(vectors, topk, nprobe, scalar_list)


if __name__ == '__main__':
    app = App()
    app.add_route('/', searcher, method='POST')

    app.run()
