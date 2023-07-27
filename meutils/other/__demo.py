#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __demo
# @Time         : 2023/7/4 09:02
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import asyncio
from aiohttp import request
from aiomultiprocess import Pool  # todo


async def get(url):
    async with request("GET", url) as response:
        return await response.text("utf-8")


async def mainmain():
    urls = ["https://www.baidu.com"] * 10  # todo: openai
    async with Pool() as pool:
        results = await pool.map(get, urls)

        return results


if __name__ == '__main__':
    # Python 3.7
    print(asyncio.run(mainmain()))  # 终端 python 可以通

    # Python 3.6
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())

    # coroutine = mainmain()
    # task = asyncio.ensure_future(coroutine)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(task)
