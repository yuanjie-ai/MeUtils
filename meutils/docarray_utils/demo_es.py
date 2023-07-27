#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2023/4/18 14:24
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.docarray_ import Document

from docarray import DocList, BaseDoc
from docarray.typing import ImageUrl, ImageTensor, NdArray
from docarray.index import HnswDocumentIndex, ElasticV7DocIndex as ElasticDocIndex

dims = 200


class Doc(BaseDoc):
    text: str
    #     embedding: NdArray = Field(dims=dims, space='cosine') # 这样不生效，奇怪
    embedding: NdArray[dims]


dl = [Doc(text=i, embedding=np.random.random((dims,)), embedding2=np.random.random((dims,))) for i in range(10000)]

index = ElasticDocIndex[Doc](hosts='http://10.211.96.37:9200', index_name='ann_test')
index.index(dl)

query = dl[0]
results, scores = index.find(query, limit=10, search_field='embedding')
list(scores - 1)
