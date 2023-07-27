#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : task01
# @Time         : 2023/7/27 08:41
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

if __name__ == '__main__':
    from ..celery_tasks import cel
else:
    from celery_tasks import cel


@cel.task
def send_msg(name):
    print("向%s发送信息..." % name)
    time.sleep(5)
    print("向%s发送信息完成" % name)
    return "信息发送成功"
