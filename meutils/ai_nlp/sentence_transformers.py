#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : sentence_transformers
# @Time         : 2023/7/4 16:11
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from sentence_transformers import SentenceTransformer as _SentenceTransformer


class SentenceTransformer(_SentenceTransformer):

    def encode_multi(self, sentences: List[str], target_devices: List[str] = None, batch_size: int = 32,
                     chunk_size: int = None):
        pool = self.start_multi_process_pool(target_devices)
        self.encode_multi_process(sentences, pool, batch_size, chunk_size)


if __name__ == '__main__':
    model = SentenceTransformer('/Users/betterme/PycharmProjects/AI/m3e-small')
    model.encode = partial(model.encode, show_progress_bar=True)
    pool = model.start_multi_process_pool()
    model.encode_multi_process(['1']*100, pool)