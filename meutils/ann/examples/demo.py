#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-ANN.
# @File         : demo
# @Time         : 2019-12-04 20:10
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

import numpy as np
from annzoo.faiss import ANN

data = np.random.random((1000, 128)).astype('float32')

ann = ANN()
ann.train(data, noramlize=True)

dis, idx = ann.search(data[:10])

# print(dis)
print(idx)

ann.write_index()
