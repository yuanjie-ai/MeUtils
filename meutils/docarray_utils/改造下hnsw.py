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
import shutil
from pathlib import Path

from docarray import BaseDoc, DocList
from docarray.typing import NdArray
from docarray.index import HnswDocumentIndex

dims = 200


class Doc(BaseDoc):
    text: str
    embedding: NdArray[dims] = Field(dims=dims, space='cosine')
    # embedding: NdArray[dims] = Field(dims=dims, space='cosine')


dl = [Doc(text=str(i), embedding=np.random.random((dims,)), embedding_=np.random.random((dims,))) for i in range(100)]

# create a Document Index
work_dir = 'test_index'
if Path(work_dir).exists():
    shutil.rmtree(work_dir)

index = HnswDocumentIndex[Doc](work_dir=work_dir)
index.index(dl)

# find similar Documents
query = dl[0]

r = index.find(query, limit=10, search_field='embedding')
df = r.documents.to_dataframe().assign(score=r.scores)
print(df)