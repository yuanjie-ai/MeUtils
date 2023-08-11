#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : pdf
# @Time         : 2023/5/18 16:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


class PageWord(BaseModel):
    x0 = 153.5
    x1 = 441.72032
    top = 76.19035999999994
    doctop = 76.19035999999994
    bottom = 92.15035999999998
    upright = True
    direction = 1
    text = "国投瑞银基金管理有限公司基金相关参数"


class PageWords(BaseModel):  # page.extract_words()
    pagewords: List[PageWord]


class Part(BaseModel):
    pass
