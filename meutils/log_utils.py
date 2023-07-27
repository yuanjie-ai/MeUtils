#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : log_utils
# @Time         : 2020/11/12 11:40 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  :

# from loguru import logger
#
# logger.add(
#     '日志同步{time: YYYY_MM_DD}.log',
#     enqueue=True,  # 异步
#     encoding="utf-8",
#     backtrace=True,
#     diagnose=True,
#     rotation='00:00',
#     retention='7 days',
# )
import os
import sys
from random import uniform
from loguru import logger
from meutils.notice.wecom import Wecom


def melogger(sink=sys.stderr, **logkwargs):  # logger.add(print, enqueue=True)
    logger.remove()
    logger.add(sink, enqueue=True, **logkwargs)


# LOG CONF: 需提前配置在环境变量里, 其他参考loguru._defaults.LOGURU_*
LOG_PATH = os.environ.get('LOG_PATH')  # python xxxx.py 才生效

# todo: http://www.manongjc.com/detail/27-wpvjqkuysjaacig.html
# 1. 过滤
# 2. 默认配置、zk配置、文件配置、环境变量配置
if LOG_PATH:
    logger.add(
        LOG_PATH,
        rotation="100 MB",
        enqueue=True,  # 异步
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
        # level=_defaults.LOGURU_LEVEL,
        # filter=_defaults.LOGURU_FILTER,
    )

else:
    logger.remove()
    logger.add(sys.stderr, enqueue=True)


# 日志采样输出：按时间 按条数
def logger4sample(log, bins=10):
    if uniform(0, bins) < 1:
        logger.info(log)


# todo: 起个服务配置通用logger
def logger4wecom(title='这是一个标题', text='这是一条log', hook_url=None):
    return Wecom(hook_url).send_markdown(title=str(title), content=str(text))


# todo:
#  add zk/es/mongo/hdfs logger
# logger = logger.patch(lambda r: r.update(name=__file__))
logger_patch = lambda name: logger.patch(lambda r: r.update(name=name))  # main模块: 等价于 __name__=__file__

if __name__ == '__main__':
    logger.info("xx")
    # logger4feishu('', 'a\nb')
    logger4wecom()

    # 异步sink

    import time, datetime
    from asgiref.sync import sync_to_async

    logger.remove()


    @sync_to_async(thread_sensitive=True)
    def sink(message):
        time.sleep(3)  # IO processing...
        print(message, end="")


    logger.add(sink, enqueue=True)


    def work():
        logger.info("Start")
        logger.info("End")
        return datetime.datetime.now()


    work()

    # 异步
    logger.remove()
    logger.add(print, enqueue=True)

