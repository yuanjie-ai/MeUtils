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

from docarray import DocList, BaseDoc
from docarray.typing import ImageUrl, ImageTensor, NdArray
from docarray.index import HnswDocumentIndex  # , ElasticV7DocIndex as ElasticDocIndex

dims = 200


class Doc(BaseDoc):
    text: str
    #     embedding: NdArray = Field(dims=dims, space='cosine') # 这样不生效，奇怪
    embedding: NdArray[dims] = Field(dims=dims, space='cosine')


#     embedding1: NdArray = Field(dims=dims)
#     embedding2: NdArray = Field(dims=dims, space='cosine')


# create some data
dl = DocList[Doc](
    [
        Doc(
            text='',
            embedding=np.random.random((dims,)),
        )
        for _ in range(1000)
    ]
)

# create a Document Index
work_dir = '/tmp/sas'
index = HnswDocumentIndex[Doc](work_dir=work_dir)

# index your data
if not Path(work_dir).exists():
    index.index(dl)  # 创建索引，第二次只加载
    index._hnsw_indices
    index._hnsw_locations

# find similar Documents
query = dl[0]

results, scores = index.find(query, limit=10, search_field='embedding')
pprint(list(zip(results, scores)))
