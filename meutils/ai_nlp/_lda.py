#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : lda
# @Time         : 2023/4/10 16:38
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from gensim import corpora, models, similarities
from gensim.models import LdaModel


def lda_model(corpus, num_topics=16, iterations=50, random_state=42, **kwargs):
    """

    :param corpus: [['w1', 'w2'], ...]
    :param num_topics:
    :param iterations:
    :param random_state:
    :param kwargs:
    :return:
    """
    dictionary = corpora.Dictionary(corpus)

    # 生成词位置和频次的组合
    _corpus = [dictionary.doc2bow(s) for s in corpus]

    # 主题模型生成
    lda = LdaModel(
        corpus=_corpus,  # 单词ID和数量的矩阵
        id2word=dictionary,  # .id2token#从单词ID映射到单词
        num_topics=num_topics,  # 主题数，也就是我们想让其生成几个主题，跟kmeans一样是无监督学习，需要指定簇的个数是一个意思
        iterations=iterations,  # 最大迭代次数
        random_state=random_state,  # 设置随机种子，保证每次模型生成的主题一样
        **kwargs
    )

    import pyLDAvis.gensim
    viz = pyLDAvis.gensim.prepare(lda, _corpus, dictionary, sort_topics=False)

    # import pyLDAvis
    # pyLDAvis.enable_notebook()
    # pyLDAvis.display(viz)
    return lda, viz

# from sklearn.datasets import fetch_20newsgroups
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
# from sklearn.decomposition import LatentDirichletAllocation
#
#
# # 加载新闻文本数据
# news = fetch_20newsgroups(subset='all')
#
# # 将文本转换为词袋模型
# cv = CountVectorizer()
# bow_corpus = cv.fit_transform(news.data)
#
# # 将词袋模型转换为TF-IDF模型
# tfidf_transformer = TfidfTransformer()
# tfidf_corpus = tfidf_transformer.fit_transform(bow_corpus)
#
#
# # 构建LDA模型
# lda_model = LatentDirichletAllocation(n_components=10,
#                                       max_iter=10, n_jobs=8,
#                                       learning_offset=50.,
#                                       random_state=0)
#
# # 训练LDA模型
# lda_model.fit(tfidf_corpus)
