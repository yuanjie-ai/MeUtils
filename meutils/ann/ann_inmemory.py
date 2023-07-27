#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ann_inmemory
# @Time         : 2023/5/15 17:50
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import numpy as np
import pandas as pd

from meutils.pipe import *
from meutils.np_utils import cosine


def ann_find(v, from_array, topk=5, threshold=0.5):
    """适合万级向量匹配"""
    if np.array(v).ndim == 1:
        v = np.array(v).reshape(1, -1)

    dist = - cosine(v, from_array)
    idxs = np.argsort(dist)[:, :topk]
    scores = - np.take_along_axis(dist, idxs, -1)
    _ = (
        pd.DataFrame(
            {
                'id': idxs[0],
                'score': scores[0],
                'embedding': from_array[idxs[0]].tolist()
            }
        )
        .query(f"score > {threshold}")
    )

    return _


if __name__ == '__main__':
    x = np.random.rand(10, 128)
    print(ann_find(x[0], x))
    print(ann_find(x[:1], x))
