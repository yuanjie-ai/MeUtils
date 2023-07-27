#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : pp
# @Time         : 2021/1/31 9:40 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import BaseConfig


class FireConf(BaseConfig):
    epoch = 10
    batch_size = 128



c = FireConf()


def f(obj={'epoch': 666}):
    return c.parse_obj(obj)

x = f()
print(x.dict())
print(c.dict())