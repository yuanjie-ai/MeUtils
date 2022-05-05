#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : ArticleInfo
# @Time         : 2020/12/2 10:44 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  :

import pandas as pd
from meutils.hash_utils import murmurhash

from typing import *
import datetime
from pydantic import BaseModel, ValidationError


class ArticleInfo(BaseModel):
    id: str = None
    title: str = None
    category: str = None
    nCategory1: List[str] = None
    subCategory: str = None
    nSubCategory1: List[str] = None
    cpApi: str = None
    cType: str = None
    source: str = None

    sourceLevel: float = None
    contentLevel: float = None
    professionalLevel: float = None
    imgNum: float = None
    titlelen: float = None
    bodyLen: float = None
    staticQuality: float = None
    dynamicQuality: float = None
    textAdScore: float = None
    pornRank: float = None
    politicalSensitive: float = None
    dedupScore: float = None
    contentScore: float = None
    authorScore: float = None

    createTime: datetime.datetime
    publishTime: datetime.datetime
    delta: float = 0

    def __init__(self, **data: Any):
        super().__init__(**data)

        self.category = self.nCategory1[0] if self.nCategory1 else None
        self.subCategory = self.nSubCategory1[0] if self.nSubCategory1 else None
        self.titlelen = len(self.title)
        self.delta = (self.createTime - self.publishTime).seconds / 3600

        # todo: 封装通用的部分
        for k in self.__dict__:
            if k not in ('id', 'title'):
                v = self.__getattribute__(k)

                if isinstance(v, str):
                    self.__setattr__(k, murmurhash(v, bins=10000))
                    # print(k)

                elif isinstance(v, datetime.datetime):
                    self.__setattr__(k, pd.Series(v).map(self._process_datetime)[0])

    def _process_datetime(self, dt):
        feats = ("year", "quarter", "month", "day", "hour", "minute", "week", "weekday", "weekofyear")
        r = []
        for feat in feats:
            _ = dt.__getattribute__(feat)
            r.append(_() if callable(_) else _)
        return r

    def return_df(self):
        return pd.DataFrame([self.dict()])


if __name__ == '__main__':
    ac = ArticleInfo(authorScore='111')
    print(ac.dict())  # 记录特征日志
    print(ac.__getattribute__('authorScore'))
