#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : word_segmentation
# @Time         : 2023/4/23 11:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from jina import Document, DocumentArray, Executor, Flow, requests, Deployment

from meutils.ai_nlp.word_segmentation import WordSegmentation


#
# class E(Executor):
#     @requests  # 默认串起来
#     def func(self, docs: DocumentArray, **kwargs):
#         print(docs.texts)
#         for d in docs:
#             d.tags = {'words': WordSegmentation('fast')(d.text)}

class E(Executor):
    @requests  # 默认串起来
    def func(self, docs: DocumentArray, **kwargs):
        print(docs.texts)


f1 = Flow(port=8501).add(uses=E)

with f1:
    # 测试
    # r = f1.post('/', DocumentArray([Document(text='我是中国人')] * 5))
    # print(r[:, 'tags'])
    # r = f1.post('/', [Document(text='我是中国人')]*5)
    # print(r.texts)

    r = f1.post('/', [Document(text='我是中国人')] * 5)
    print(r.texts)
