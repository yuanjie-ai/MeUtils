#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : SentenceEncoder
# @Time         : 2023/6/7 09:09
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from jina import requests, dynamic_batching, Document, DocumentArray, Executor, Deployment, Flow, Client
from sentence_transformers import SentenceTransformer
import torch


class DummyExecutor(Executor):
    c = Client(host='grpc://0.0.0.0:51234', asyncio=True)

    @requests
    async def process(self, docs: DocumentArray, **kwargs):
        self.c.post('/', docs)


class SentenceEncoder(Executor):
    """A simple sentence encoder that can be run on a CPU or a GPU

    :param device: The pytorch device that the model is on, e.g. 'cpu', 'cuda', 'cuda:1'
    """

    def __init__(self, device: str = 'cpu', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
        self.model.to(device)  # Move the model to device

    @requests
    @dynamic_batching(preferred_batch_size=10, timeout=1_000)  # 默认10s
    def encode(self, docs: DocumentArray, **kwargs):
        """Add text-based embeddings to all documents"""
        with torch.inference_mode():
            embeddings = self.model.encode(docs.texts, batch_size=32)
        docs.embeddings = embeddings



def main(inputs=['x']):
    dep = Deployment(uses=SentenceEncoder, uses_with={'device': 'cpu'})

    with dep:
        dep.post(on='/encode', inputs=inputs)


if __name__ == '__main__':

    def generate_docs():
        for _ in range(2):
            yield Document(
                text='Using a GPU allows you to significantly speed up encoding.'
            )


    main()
