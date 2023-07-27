#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : word_segmentation
# @Time         : 2023/4/23 11:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from paddlenlp import Taskflow


# 增加停用词
# 增加词频统计
# 增加共现矩阵
# 数据清洗机制 只提取中文 简繁转换 半角全角 大小写

@lru_cache()
class WordSegmentation(object):

    def __init__(self, mode='fast', user_dict=None, batch_size=32, device='cpu', filter_func=None, show_bar=False):
        """https://github.com/PaddlePaddle/PaddleNLP/blob/develop/docs/model_zoo/taskflow.md#%E4%B8%AD%E6%96%87%E5%88%86%E8%AF%8D

        :param mode:
            base 实体粒度分词，在精度和速度上的权衡，基于百度LAC
            fast 最快：实现文本快速切分，基于jieba中文分词工具
            accurate wordtag
            精确模式————最准：实体粒度切分准确度最高，基于百度解语, 精确模式基于预训练模型，更适合实体粒度分词需求，适用于知识图谱构建、企业搜索Query分析等场景中

        :param user_dict:
            在快速模式下，词典文件每一行为一个自定义item+"\t"+词频（词频可省略，词频省略则自动计算能保证分出该词的词频），暂时不支持黑名单词典（即通过设置”年“、”末“，以达到切分”年末“的目的）。
                平原上的火焰  10

            在base模式和精确模式下，词典文件每一行由一个或多个自定义item组成。
                平原上的火焰
                上 映

            在lac词性标注下，你可以通过装载自定义词典来定制化分词和词性标注结果。词典文件每一行表示一个自定义item，可以由一个单词或者多个单词组成，单词后面可以添加自定义标签，格式为item/tag，如果不添加自定义标签，则使用模型默认标签n。
                赛里木湖/LAKE
                高/a 山/n
                海拔最高

        :param filter_func:
            lambda w: w not in stopwords
        """
        self.batch_size = max(batch_size, 2)
        self.filter_func = filter_func
        self.show_bar = show_bar

        self.task_flow = Taskflow(
            "word_segmentation",
            mode=mode,
            batch_size=batch_size,
            user_dict=user_dict,
            device=device
        )

    def __call__(self, texts):
        results = texts | xbar4iter(self._task_flow, self.batch_size, show_bar=self.show_bar)

        if self.filter_func:  # 每一条都过滤
            results = results | xmap_(lambda ws: ws | xfilter_(self.filter_func))  # 重写过滤逻辑
        return results

    def _task_flow(self, texts):
        if isinstance(texts, str):
            texts = [texts]

        _ = self.task_flow(texts)
        if len(texts) == 1:
            return [_]
        return _


if __name__ == '__main__':
    print(WordSegmentation('fast', filter_func=lambda w: w not in ('的'))('我的中国人'))
    print(WordSegmentation('fast', filter_func=lambda w: w not in ('的'))(['我的中国人']))
    print(WordSegmentation('fast', filter_func=lambda w: w not in ('的'))(['我的中国人'] * 2))
    print(WordSegmentation('fast')(['我的中国人'] * 2))
    print(WordSegmentation('fast')(['我的中国人']))
    print(WordSegmentation('fast')('我的中国人'))
