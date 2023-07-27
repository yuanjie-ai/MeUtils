#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : ai
# @Time         : 2021/4/13 11:19 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 不行


import tensorflow as tf
from meutils.pipe import *


def compile(strategy=tf.distribute.MirroredStrategy(), **compile_kwargs):
    """

    :param strategy: 单机多卡
    :param compile_kwargs: compile参数，loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"]
    :return:
    """

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        if strategy is None:
            model = wrapped(*args, **kwargs)
            model.compile(**compile_kwargs)
            return model
        else:
            logger.info(f'Number of devices: {strategy.num_replicas_in_sync}')
            with strategy.scope():
                model = wrapped(*args, **kwargs)
                model.compile(**compile_kwargs)
                return model

    return wrapper


if __name__ == '__main__':
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.models import Sequential


    @compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    def create_model():
        """from tensorflow.python.keras.models import clone_and_build_model"""
        model = Sequential()
        model.add(Dense(12, input_dim=20, kernel_initializer="uniform", activation="relu"))
        model.add(Dense(8, kernel_initializer="uniform", activation="relu"))
        model.add(Dense(1, kernel_initializer="uniform", activation="sigmoid"))
        return model


    print(create_model().summary())
