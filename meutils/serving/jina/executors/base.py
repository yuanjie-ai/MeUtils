#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : base
# @Time         : 2023/7/24 14:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from jina import Executor, Deployment, Flow, Client
from jina import requests, dynamic_batching
from docarray import DocList
from docarray.documents import TextDoc, ImageDoc


class MyExecutor(Executor):
    @requests
    # @dynamic_batching()
    def foo(self, docs: list, **kwargs):
        for d in docs:
            d.text = 'hello world'
        return docs


if __name__ == '__main__':
    # f1 = Flow(port=8501).add(uses=MyExecutor)
    #
    # with f1:
    #     response_docs = f1.post(
    #         on='/',
    #         inputs=DocList[TextDoc]([TextDoc(text='hello')]),
    #         return_type=DocList[TextDoc]
    #     )
    #     print(f'Text: {response_docs[0].text}')

    e = MyExecutor()
    # print(e.foo(DocList[TextDoc]([TextDoc(text='hello')]))[0].text)
    print(e.foo([TextDoc(text='hello')])[0].text)
