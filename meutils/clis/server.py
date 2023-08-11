#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : cli_fastapi
# @Time         : 2023/8/4 15:01
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *


@cli.command()  # help会覆盖docstring
def celery_consumer(host='0.0.0.0', port: int = 8501):
    """
    # 消费者
    celery -A meutils.serving.celery.tasks worker -l info

    # 生产者
    mecli-server --host 127.0.0.1 --port 8000

    """

    from meutils.serving.fastapi import App
    from meutils.serving.celery.router import router

    app = App()
    app.include_router(router)
    app.run(host=host, port=port)


if __name__ == '__main__':
    cli()
