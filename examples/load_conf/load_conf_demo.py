#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : load_conf_demo
# @Time         : 2021/1/27 8:38 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *


class Config(BaseConfig):
    name: str = ''
    age: int = 666
    betterme: List[str]=[]


c = Config.parse_zk('/push/myconf')


print(Besttable.draw_dict(c.dict()))

# print(Config.parse_yaml('./myconf.yaml').dict())
#
# print(Config.parse_zk('/push/bot').betterme)
# print(Config.parse_zk('/push/bot').__getattribute__('betterme'))

# os.environ['name'] = '123456789'
# print(Config.parse_env().dict())
