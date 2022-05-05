#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : pydantic_demo
# @Time         : 2021/1/27 8:41 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : https://blog.csdn.net/swinfans/article/details/89629641
# https://blog.csdn.net/codename_cys/article/details/107675748

import yaml
from meutils.pipe import *
from pydantic import BaseModel


class Config(BaseModel):
    name: str
    age: int = 666


c = Config(name='name')
# json
c = Config.parse_file('./load_conf/myconf.json')

# yaml
c = Config.parse_obj(yaml_load('./load_conf/myconf.yaml'))
print(c.dict())



os.environ['name'] = 'environ'

print(Config.parse_obj(os.environ).dict())

