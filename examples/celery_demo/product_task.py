#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : product_task
# @Time         : 2023/7/27 09:02
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 写成服务
import pickle

from meutils.pipe import *
from tasks.task01 import send_msg


for i in range(10):
    send_msg.delay('xxx')
