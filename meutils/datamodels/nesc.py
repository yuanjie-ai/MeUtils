#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : nesc
# @Time         : 2022/4/29 上午9:06
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from typing import *
from pydantic import BaseModel


class Item(BaseModel):
    itemId: str = None
    traceId: str = 'rec'
    code1: str = None
    code2: str = None





def f(a: str) -> Optional[str]:
    return None