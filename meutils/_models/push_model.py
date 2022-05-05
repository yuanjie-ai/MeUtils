#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : push_model
# @Time         : 2021/3/8 2:37 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *


class PushItemModel(BaseConfig):
    itemId:str
    pushId:str
    title:str
    subTitle:str
    userCategory: List[str]


class PushItemModels(BaseConfig):
    pushItemModels: List[PushItemModel]
