#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : retry_demo
# @Time         : 2021/2/3 12:18 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : https://www.cnblogs.com/wuzhibinsuib/p/13443622.html

from meutils.pipe import *
from tenacity import retry, stop_after_delay, stop_after_attempt

a = 0

s = time.time()


# @retry(stop=stop_after_delay(0.001) | stop_after_attempt(100), reraise=True)  # reraise抛出原始错误
# def test_retry():
#     global a
#     a += 1
#     print(f"请求第{a}次")
#     print(time.time() - s)
#
#     raise Exception
#
#
# test_retry()


# from tenacity import retry, stop_after_attempt, retry_if_result
#
# def return_last_value(retry_state):
#     print("执行回调函数")
#     return retry_state.outcome.result()  #表示原函数的返回值
#
# def is_false(value):
#     return value is False
#
# @retry(stop=stop_after_attempt(3), retry_error_callback=return_last_value,
#        retry=retry_if_result(is_false))
# def test_retry():
#     print("等待重试.....")
#     return False
#
# print(test_retry())

# from meutils.http_utils import request
#
# request()


if __name__ == '__main__':
    print(__file__)