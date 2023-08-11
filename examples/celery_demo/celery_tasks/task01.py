#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : task01
# @Time         : 2023/7/27 08:41
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import requests

from meutils.pipe import *

if __name__ == '__main__':
    from ..celery_tasks import cel
else:
    from celery_tasks import cel


@cel.task
def proxy_task(name, url='http://ocr', json=None):
    print("向%s发送邮件..." % name)
    time.sleep(5)  ####### 调的ocr: 代理服务
    requests.post(url, json=json)  # 任何任务： nlp ocr ...

    print("向%s发送邮件完成" % name)
    return "邮件发送成功"


@cel.task
def func_task(fn_pkl):
    logger.debug(fn_pkl)

    fn = pickle.loads(fn_pkl)
    return fn
