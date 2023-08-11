#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : task01
# @Time         : 2023/7/27 08:41
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://blog.csdn.net/weixin_43354181/article/details/126753700

from meutils.pipe import *

from celery import shared_task

"""https://blog.csdn.net/weixin_43354181/article/details/126753700
retry_backoff_max: 重试的最大的间隔时间，比如重试次数设置的很大，retry_backoff 的间隔时间重复达到了这个值之后就不再增大了。
这个值默认是 600s，也就是 10分钟。

如果需要任务延时的间隔值是按照 retry_backoff 和 retry_backoff_max 两个设定值来运行，那么则需要将 retry_jitter 值设为 False。

retry_backoff 参数可以设置成一个 布尔型数据，为 True 的话，自动重试的时间间隔会成倍的增长

default_retry_delay=10

"""


@shared_task(autoretry_for=(Exception,), retry_backoff=True, default_retry_delay=3, retry_kwargs={'max_retries': 3})
def send_msg(name):
    print("向%s发送信息..." % name)
    time.sleep(5)
    print("向%s发送信息完成" % name)
    return "信息发送成功"

