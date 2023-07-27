#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : 异步任务
# @Time         : 2023/5/30 12:00
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import typing

import anyio

if sys.version_info >= (3, 10):  # pragma: no cover
    from typing import ParamSpec
else:  # pragma: no cover
    from typing_extensions import ParamSpec

T = typing.TypeVar("T")
P = ParamSpec("P")


def is_async_callable(obj: typing.Any) -> bool:
    while isinstance(obj, functools.partial):
        obj = obj.func

    return asyncio.iscoroutinefunction(obj) or (
            callable(obj) and asyncio.iscoroutinefunction(obj.__call__)
    )


async def run_in_threadpool(func: typing.Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    if kwargs:  # pragma: no cover
        # run_sync doesn't accept 'kwargs', so bind them in here
        func = functools.partial(func, **kwargs)
    return await anyio.to_thread.run_sync(func, *args)


class BackgroundTask:
    def __init__(
            self, func: typing.Callable[P, typing.Any], *args: P.args, **kwargs: P.kwargs
    ) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.is_async = is_async_callable(func)

    async def __call__(self) -> None:
        if self.is_async:
            await self.func(*self.args, **self.kwargs)
        else:
            await run_in_threadpool(self.func, *self.args, **self.kwargs)


class BackgroundTasks(BackgroundTask):
    def __init__(self, tasks: typing.Optional[typing.Sequence[BackgroundTask]] = None):
        self.tasks = list(tasks) if tasks else []

    def add_task(
            self, func: typing.Callable[P, typing.Any], *args: P.args, **kwargs: P.kwargs
    ) -> None:
        task = BackgroundTask(func, *args, **kwargs)
        self.tasks.append(task)

    async def __call__(self) -> None:
        for task in self.tasks:
            await task()


if __name__ == '__main__':
    @timer('test')
    def task(x):
        logger.info(x)
        time.sleep(3)
        print(x)


    bt = BackgroundTasks()
    bt.add_task(task, 1)
    bt.add_task(task, 2)

    print('xxxxxxxxxxxxxxx')

    # loop = asyncio.get_event_loop()
    # _ = asyncio.gather(bt())  # asyncio.wait(tasks)
    # loop.run_until_complete(_)
    #
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.wait([bt]))
    # loop.close()
    import asyncio
    asyncio.run(bt())
    print('xxxxxxxxxxxxxxx')
