#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : try
# @Time         : 2021/4/2 11:03 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
from meutils.pipe import *
from meutils.log_utils import logger4wecom


def wecom_hook(title='Task Done', text=None, hook_url=None):
    """装饰器里不可变参数

    :param title:
    :param text: 如果为空，用函数返回值填充【text覆盖函数返回值】
    :param hook_url: hook_url或者群名称
    :return:
    """

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        s = time.time()
        r = wrapped(*args, **kwargs)
        e = time.time()

        mins = (e - s) // 60

        logger.info(f"{title} done in {mins} m")

        logger4wecom(
            title=title,
            text=f"**{wrapped.__name__}:** {r if text is None else text}\n耗时 {mins} m",
            hook_url=hook_url
        )

        return r

    return wrapper


def wecom_catch(hook_url=None, more_info=True):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        try:
            return wrapped(*args, **kwargs)

        except Exception as e:
            info = traceback.format_exc() if more_info else e
            text = f"""
            ```
            {info.strip()}
            ```
            """.strip()
            logger4wecom(wrapped.__name__, text, hook_url)

    return wrapper


if __name__ == '__main__':
    # @feishu_catch()
    # def f():
    #     1 / 0
    #
    #
    # f()

    # @wecom_catch(more_info=False)
    # def f():
    #     1 / 0
    #
    #
    # f()

    @wecom_hook('catch_hook测试', text="TEXT")
    @wecom_catch()
    def f():
        # 1 / 0
        print(time.time())
        return 'RES'


    f()
