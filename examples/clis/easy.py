#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : eazy
# @Time         : 2021/1/31 9:43 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *


class TrainConf(BaseConfig):
    epoch = 10
    batch_size = 128


def train(**kwargs):
    logger.info("开始训练")
    time.sleep(3)


def run(**kwargs):
    logger.info(f"kwargs: {kwargs}")
    c = TrainConf.parse_obj(kwargs)
    train(**c.dict())


if __name__ == '__main__':
    import fire

    fire.Fire(run)  # python ./fire_args.py gen --x 100
    # fire.Fire() # python fire_args.py --x 10000
