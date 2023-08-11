#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : bserver
# @Time         : 2023/8/1 13:01
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from fastapi import FastAPI, APIRouter, Request

from meutils.serving.fastapi import App
from meutils.pipe import *
app = App()


@app.post('/', name='xxxx')
async def f(body: Request):
    logger.debug(await body.body())
    logger.debug(await body.json())






    return


app.run(port=9944)
