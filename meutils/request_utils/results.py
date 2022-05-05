#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : result
# @Time         : 2021/2/18 6:16 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.zk_utils import zk_cfg
from meutils.request_utils import request


def get_ac(docid, parser=lambda x: x.get('item', {})):
    return request(f"{zk_cfg.ac_url}/{docid}", parser=parser)


def get_acs(docids, max_workers=10, parser=lambda x: x.get('item', {}).get('title')):
    func = functools.partial(get_ac, parser=parser)
    return docids | xThreadPoolExecutor(func, max_workers) | xlist


def get_simbert_vectors(sentences, url=None, json=None):
    """适合小批量请求
    :param sentences:
    :return:

        vectors_list = sentences_list | xThreadPoolExecutor(request_func, max_workers)
        np.row_stack(vectors_list)
    """
    if url is None:
        url = 'http://10.210.10.94:32651/simbert' if is_open() else 'http://10.211.10.33:32520/simbert'
    if json is None:
        json = {'sentences': sentences}

    data = request(url, json).get('vectors')

    return np.array(data, 'float32')


if __name__ == '__main__':
    print(get_acs(['fengxing_144094389']))

    # print(get_simbert_vectors('bert向量化', is_lite='1').shape)
