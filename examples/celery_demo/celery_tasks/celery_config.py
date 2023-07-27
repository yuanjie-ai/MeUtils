#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : celery_config
# @Time         : 2023/7/27 08:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

BROKER_URL = 'redis://localhost:6379/1'

CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'

CELERY_TIMEZONE = 'Asia/Shanghai'  # 不指定时区的话默认采用UTC

# 导入指定的任务模块
CELERY_IMPORTS = (
    'celerywithconfig.task1',
    'celerywithconfig.task2',
)
