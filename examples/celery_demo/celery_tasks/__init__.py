#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tasks
# @Time         : 2023/7/27 08:38
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from celery import Celery
#
# app = Celery('wedo')  # 创建 Celery 实例
# app.config_from_object('wedo.config')
#
# # 配置 wedo.config
# # config.py
# BROKER_URL = 'redis://10.8.238.2:6379/0'  # Broker配置，使用Redis作为消息中间件
# CELERY_RESULT_BACKEND = 'redis://10.8.238.2:6379/0'  # BACKEND配置，这里使用redis
# CELERY_RESULT_SERIALIZER = 'json'  # 结果序列化方案
# CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24  # 任务过期时间
# CELERY_TIMEZONE = 'Asia/Shanghai'  # 时区配置
# CELERY_IMPORTS = (  # 指定导入的任务模块,可以指定多个
#     'wedo.tasks',
#     'wedo.period_task'
# )

from celery import Celery

cel = Celery(
    'celery_demo',
    broker='redis://127.0.0.1:6379',
    backend='redis://127.0.0.1:6379',
    include=[
        'celery_tasks.task01',
        'celery_tasks.task02'
    ])  # 通过celery实例加载配置模块cel.config_from_object('celery_tasks.celery_config')
