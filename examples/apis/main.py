#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : main
# @Time         : 2023/5/31 13:36
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 
from fastapi import FastAPI, APIRouter

from meutils.pipe import *
from meutils.serving.fastapi import App

app = App()


@app.get('/', name='xxxx')
def f():
    return {'1': '2'}


# app.include_router(router)
# app.run()
