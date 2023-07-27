#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : lda
# @Time         : 2023/6/6 10:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


class LDA(object):

    def __init__(self, tokenizer=lambda x: x, **cv_kwargs):
        self.vectorizer = CountVectorizer(tokenizer=tokenizer, lowercase=False, **cv_kwargs)

    def fit(self, texts, n_components=5, **lda_kwargs):
        self.X = self.vectorizer.fit_transform(texts)
        self.lda_model = LatentDirichletAllocation(n_components=n_components, **lda_kwargs)
        self.lda_model.fit(self.X)

    def viz(self, file=''):
        import pyLDAvis
        import pyLDAvis.sklearn

        # 可视化LDA主题模型
        pyLDAvis.enable_notebook()

        vis = pyLDAvis.sklearn.prepare(self.lda_model, self.X, self.vectorizer)
        if file:
            pyLDAvis.save_html(vis, file)

        return vis
