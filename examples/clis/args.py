#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : p
# @Time         : 2021/1/31 9:31 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import BaseConfig


class FireConf(BaseConfig):
    epoch = 10
    batch_size = 128



c = FireConf()
def gen(**kwargs):
    c.parse_obj(kwargs)
    print(c.dict())


if __name__ == '__main__':

    from fire import Fire


    Fire(gen, name='FireConf')
    # Fire(FireConf(), name='FireConf')