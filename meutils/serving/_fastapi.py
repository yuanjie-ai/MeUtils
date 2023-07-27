#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : _fastapi
# @Time         : 2023/4/28 13:08
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.str_utils import json_loads

from fastapi.responses import Response, StreamingResponse
from fastapi import FastAPI, Form, Depends, File, UploadFile, Body, Request, BackgroundTasks


class App(FastAPI):

    def __init__(self, title: str = "Meutils API", **kwargs):
        super().__init__(title=title, **kwargs)

    def run(self, app=None, host="0.0.0.0", port=8000, workers=1, access_log=True, reload=False, app_dir=None, **kwargs):
        """
        :param app:   app字符串可开启热更新 debug/reload
        """
        import uvicorn

        uvicorn.config.LOGGING_CONFIG['formatters']['access']['fmt'] = f"""
              🔥 %(asctime)s - %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s
              """.strip()
        uvicorn.run(
            app or self,
            host=host, port=port, workers=workers, access_log=access_log, reload=reload, app_dir=app_dir, **kwargs
        )

    def register(self, handler_func, path=None, methods=None, prefix='', **api_route_kwargs):  # add_route注册服务
        """

        :param handler_func: 自定义 handler_func
        :param path:
        :param methods:
        :return:
        """
        path = path or f"{handler_func.__name__.replace('_', '-')}"
        path = (Path('/') / Path(prefix) / Path(path)).as_posix()

        self.handler_func = handler_func
        self.api_route(path=path, methods=methods, **api_route_kwargs)(self.handler)

    async def handler(self, request: Request):  # 处理一切入参
        """可重写"""
        input = request.query_params._dict
        body = await request.body()

        if body.startswith(b'{'):  # 主要分支 # json={}
            input.update(json_loads(body))  # json_loads

        query = input.get('query', '')

        if inspect.isgeneratorfunction(self.handler_func):
            return StreamingResponse(self.handler_func(query), media_type='text/event-stream')  # 流式接口

        return self.handler_func(query)


if __name__ == '__main__':

    def gen_data(query):
        for i in range(5):
            time.sleep(i)
            yield f"{query} {i}\n"


    app = App()
    app.register(gen_data, '/x')

    app.run()
