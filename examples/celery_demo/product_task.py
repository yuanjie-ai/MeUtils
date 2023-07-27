#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : product_task
# @Time         : 2023/7/27 09:02
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from celery_tasks.task01 import send_email
from celery_tasks.task02 import send_msg

for i in range(10):
    task = send_email.delay(i)
    logger.info(f"Task: {task.id}")
    task = send_msg.delay(i)
    logger.info(f"Task: {task.id}")
