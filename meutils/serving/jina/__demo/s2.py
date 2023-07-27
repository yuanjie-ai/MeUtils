#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : s2
# @Time         : 2023/7/24 14:16
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.pipe import *
from jina import Executor, requests, Deployment
from docarray import DocList
from docarray.documents import TextDoc


class MyExecutor(Executor):
    @requests
    def foo(self, docs: DocList[TextDoc], **kwargs) -> DocList[TextDoc]:
        for d in docs:
            d.text = 'hello world'
        # return docs


from jina import requests, dynamic_batching, Document, DocumentArray, Executor, Deployment, Flow, Client

f1 = Flow(port=8501).add(uses=MyExecutor)

with f1:
    response_docs = f1.post(
        on='/',
        inputs=DocList[TextDoc]([TextDoc(text='hello')]),
        return_type=DocList[TextDoc]
    )
    print(f'Text: {response_docs[0].text}')

