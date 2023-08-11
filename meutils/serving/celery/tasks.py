#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : app
# @Time         : 2023/8/4 11:15
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://blog.csdn.net/weixin_43354181/article/details/126753700
# https://blog.csdn.net/weixin_43047908/article/details/128383893


from meutils.pipe import *
from celery import Celery, shared_task

############################################################
CELERY_BROKER = os.getenv('CELERY_BROKER', 'redis://127.0.0.1:6379')
CELERY_BACKEND = os.getenv('CELERY_BACKEND', CELERY_BROKER)
CELERY_MAX_RETRIES = int(os.getenv('CELERY_MAX_RETRIES', 6))
############################################################

app = Celery(
    'MeutilsCelery',
    broker=CELERY_BROKER,
    backend=CELERY_BACKEND,
)

app.conf.update(
    result_expires=30 * 24 * 60 * 60,
    enable_utc=False,
    timezone='Asia/Shanghai',
    task_track_started=True,
)


# app.config_from_envvar
# app.config_from_cmdline

@shared_task()
def do_task(**kwargs):
    return kwargs


@shared_task(
    autoretry_for=(Exception,),

    retry_backoff=True,
    # retry_backoff_max=60, # 2 ** max_retries
    retry_jitter=False,

    retry_kwargs={'max_retries': CELERY_MAX_RETRIES}
)
def proxy_task(**kwargs):
    method = kwargs.pop('method', '')
    url = kwargs.pop('url', '')

    response = requests.request(method, url, **kwargs).json()

    return response
