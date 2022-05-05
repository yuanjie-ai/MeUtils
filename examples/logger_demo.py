#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : demo
# @Time         : 2019-12-10 17:24
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

"""
配合：https://github.com/notifiers/notifiers
https://www.jianshu.com/p/2945634fe349
"""
from loguru import logger

trace = logger.add('x.log')  # 输出日志到文件
logger.debug('this is a debug message')
logger.remove(trace)  # 中断写入文件
logger.debug('写不进去了')

# 时间格式化
logger.add("file.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

# 字符串格式化
logger.info('If you are using Python {}, prefer {feature} of course!', 3.6, feature='f-strings')

# compression
logger.add("file_Y.log", compression="zip")  # 保存zip格式

logger.add("somefile.log", enqueue=True)  # 异步写入
logger.add("somefile.log", serialize=True)  # 序列化为json

# retention
logger.add('runtime.log', retention='10 days')  # 一段时间后会清空

# rotation
from loguru import logger

logger.add('runtime_{time}.log', rotation="500 MB")  # 每 500MB 存储一个文件
logger.add('runtime_{time}.log', rotation='00:00')  # 每天 0 点新创建一个 log 文件
logger.add('runtime_{time}.log', rotation='1 week')  # 每隔一周创建一个 log 文件


# Traceback
@logger.catch
def my_function(x, y, z):
    # An error? It's caught anyway!
    return 1 / (x + y + z)


from loguru import logger

trace = logger.add('runtime_{time}.log', rotation="100 MB", retention='10 days')
logger.debug('this is a debug message')
if __name__ == '__main__':
    with logger.catch():
        my_function()
