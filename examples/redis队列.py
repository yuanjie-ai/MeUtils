#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : redis队列
# @Time         : 2023/6/9 15:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import time

from meutils.pipe import *
from redis import Redis
from rq import Connection, Queue, Worker




if __name__ == '__main__':
    # Tell rq what Redis connection to use
    with Connection():
        q  = Queue(connection=Redis())

        Worker(q).work()