#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : _run_fastapi
# @Time         : 2023/8/4 14:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


# from tasks import *
from meutils.serving.fastapi import App
from meutils.serving.celery.router import router

app = App()
app.include_router(router)
app.run(port=8899)
