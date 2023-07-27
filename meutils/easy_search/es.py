#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : es
# @Time         : 2023/3/14 上午10:38
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import pandas as pd
from whoosh import scoring
from whoosh.fields import *
from whoosh.filedb.filestore import FileStorage

from jieba.analyse import ChineseAnalyzer

# ME
from meutils.pipe import *


class EasySearch(object):

    def __init__(self, indexdir='whoosh_index', indexname='MAIN'):
        Path(indexdir).mkdir(parents=True, exist_ok=True)

        self.storage = FileStorage(indexdir)
        self.indexname = indexname

        self.ix = None
        if self.storage.index_exists(indexname=indexname):
            self.ix = self.storage.open_index(indexname)

    def create_index(self, df: pd.DataFrame, schema, procs=4, limitmb=1024 * 2):
        self.ix = self.storage.create_index(schema, indexname=self.indexname)
        writer = self.ix.writer(procs=procs, multisegment=True, limitmb=limitmb)
        for fields in tqdm(df.to_dict(orient='records'), 'Create Index'):
            writer.add_document(**fields)
        writer.commit()

    def find(self, defaultfield, querystring, limit=5, weighting=scoring.BM25F, **kwargs):
        """

        @param defaultfield:
        @param querystring:
        @param limit:
        @param weighting: scoring.BM25F or scoring.TF_IDF()
        @param kwargs:
        @return:
        """
        assert self.ix is not None, 'please specify index !!!'

        with self.ix.searcher(weighting=weighting) as searcher:
            hits = searcher.find(defaultfield, querystring, limit=limit, **kwargs)
            df = pd.DataFrame([{**hit.fields(), 'score': hit.score} for hit in hits])
            df['runtime'] = hits.runtime

            return df


if __name__ == '__main__':
    from whoosh.fields import *

    df = pd.DataFrame([{'id': '1', 'text': '周杰伦'}] * 10)
    schema = Schema(
        id=ID(stored=True),
        text=TEXT(stored=True, analyzer=ChineseAnalyzer(cachesize=-1))  # 无界缓存加速
    )

    es = EasySearch('index')
    es.create_index(df, schema)
    print(es.find('text', '周杰伦'))
