#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : conf
# @Time         : 2021/1/31 10:20 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *


# 定义参数
class TrainConf(BaseConfig):
    epoch = 10
    batch_size = 128


def train(**kwargs):
    logger.info("开始训练")
    time.sleep(3)


# 使用参数
def run(**kwargs):
    logger.info(f"输入参数: {kwargs}")
    c = TrainConf.parse_obj(kwargs)
    logger.info(f"使用参数: {c.dict()}")
    train(**c.dict())


# 传入参数
conf_cli = lambda: fire.Fire(run)  # <conf_cli> --epoch 11 --batch_size 111
# fire.Fire()需要指定命令对象
