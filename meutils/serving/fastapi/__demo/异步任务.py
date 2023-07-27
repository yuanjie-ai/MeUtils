#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : 异步任务
# @Time         : 2023/5/29 09:58
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import time

from meutils.pipe import *

from fastapi.responses import Response, StreamingResponse, JSONResponse, RedirectResponse
from fastapi import FastAPI, Form, Depends, File, UploadFile, Body, Request, BackgroundTasks

app = FastAPI()


def task():
    logger.info(f"开始：{time.ctime()}")
    time.sleep(3)
    logger.info(f"结束：{time.ctime()}")


@app.get("/")
async def completions(background_tasks: BackgroundTasks):
    background_tasks.add_task(task)
    logger.info(f"##### 请求: {time.ctime()}")

    return {'a': time.ctime()}

@app.options("/example")
async def options_example(response: Response):
    logger.info(response.headers)
    response.headers["Allow"] = "GET, POST, PUT, DELETE, OPTIONS"
    return {'a': 1}
@app.options("/v1/chat/completions")
async def options_chat_completions(request: Request, response: Response):
    # logger.info(await request.body())


    # response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    # response.headers["Allow"] = "GET, POST, OPTIONS"
    # response.headers["Allow"] = "GET, POST, OPTIONS"

    return {'a': 1} # RedirectResponse("/")


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
