#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2023/5/26 09:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.middleware.cors import CORSMiddleware

from meutils.serving.fastapi.errors.http_error import http_error_handler
from meutils.serving.fastapi.errors.validation_error import http422_error_handler


class App(FastAPI):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
        self.add_exception_handler(HTTPException, http_error_handler)
        self.add_exception_handler(RequestValidationError, http422_error_handler)

    def include_router(self, router, prefix='', **kwargs):
        super().include_router(router, prefix=prefix, **kwargs)

    def run(self, app=None, host="0.0.0.0", port=8000, workers=1, access_log=True, reload=False, **kwargs):
        """

        :param app:   app字符串可开启热更新 reload
        :param host:
        :param port:
        :param workers:
        :param access_log:
        :param kwargs:
        :return:
        """

        import uvicorn

        uvicorn.config.LOGGING_CONFIG['formatters']['access']['fmt'] = f"""
        🔥 %(asctime)s - %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s
        """.strip()
        uvicorn.run(
            app if app else self,
            host=host, port=port, workers=workers, access_log=access_log, reload=reload, **kwargs
        )


if __name__ == '__main__':
    from fastapi import FastAPI, APIRouter

    app = App()
    router = APIRouter()


    @router.get('/', name='xxxx')
    def f():
        return {'1': '2'}


    app.include_router(router)
    app.run(port=8899)
