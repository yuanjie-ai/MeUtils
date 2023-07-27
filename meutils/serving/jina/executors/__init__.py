#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : executors
# @Time         : 2023/6/6 15:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from jina import Document, DocumentArray, Executor, Flow, requests, Deployment
from sentence_transformers import SentenceTransformer

model_name_or_path = 'intfloat/multilingual-e5-base'

model = SentenceTransformer(model_name_or_path)

encode = lru_cache()(model.encode)
class Parameters(BaseModel):
    model: str
    batch_size: int

class E(Executor):
    @requests(on='/encode')
    def func(self, docs: DocumentArray, parameters, **kwargs):  # 客户端参数
        embeddings = encode(docs.texts, batch_size=32, normalize_embeddings=True)
        for doc, embedding in zip(docs, embeddings):
            doc.embedding = embedding
            # background_tasks.add_task(encode(doc.text, normalize_embeddings=True))


f1 = Flow(port=8501).add(uses=E)

with f1:
    # 测试
    # r = f1.post('/', DocumentArray([Document(text='我是中国人')] * 5))
    # print(r[:, 'tags'])
    # r = f1.post('/', [Document(text='我是中国人')]*5)
    # print(r.texts)

    # r = f1.post('/encode', DocumentArray([Document(text='我是中国人')] * 5))
    # print(r.texts)
    # print(r.embeddings)
    f1.block()
