#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : in_memory
# @Time         : 2023/4/27 10:33
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from docarray import DocList, BaseDoc
from docarray.typing import TorchTensor
from docarray.utils.find import find
from docarray.utils.filter import filter_docs


class Document(BaseDoc):
    text: str
    embedding: TorchTensor

    DocList[Document]
    def find(self, query, topk=5, threshold=0.66):  # 返回df
        v = self.encode(query)  # np

        if self.backend == 'in_memory':
            r = self.index.find(TorchTensor(v), topk)
            self._df = (
                # r.documents.to_dataframe() # bug
                pd.DataFrame(json.loads(r.documents.to_json()))
                .assign(score=r.scores)
                .query(f'score > {threshold}')
            )

        return self._df


