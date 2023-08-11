#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : http_utils
# @Time         : 2020/11/12 11:49 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : request cache https://mp.weixin.qq.com/s/9v9u4FhUtF8ivcu7Zj9NTQ

from tenacity import retry, stop_after_delay, stop_after_attempt, wait_fixed

# ME
from meutils.pipe import *


@retry(wait=wait_fixed(2),  # 重试之前等待2秒
       stop=stop_after_delay(7) | stop_after_attempt(3),  # 同时满足用 | 没毛病：重试7秒重试3次
       retry_error_callback=logger.error,
       reraise=True)
def request4retry(url, method='get', return_json=True, timeout=3, encoding=None, **kwargs):
    """None or {}"""
    logger.info("Try")

    _kwargs = {}
    _kwargs['timeout'] = timeout
    _kwargs['headers'] = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE '
    }
    r = requests.request(method, url, **{**_kwargs, **kwargs})
    r.encoding = encoding if encoding else r.apparent_encoding

    return r.json() if return_json else r
# def _create_retry_decorator(embeddings: OpenAIEmbeddings) -> Callable[[Any], Any]:
#     import openai
#
#     min_seconds = 4
#     max_seconds = 10
#     # Wait 2^x * 1 second between each retry starting with
#     # 4 seconds, then up to 10 seconds, then 10 seconds afterwards
#     return retry(
#         reraise=True,
#         stop=stop_after_attempt(embeddings.max_retries),
#         wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
#         retry=(
#             retry_if_exception_type(openai.error.Timeout)
#             | retry_if_exception_type(openai.error.APIError)
#             | retry_if_exception_type(openai.error.APIConnectionError)
#             | retry_if_exception_type(openai.error.RateLimitError)
#             | retry_if_exception_type(openai.error.ServiceUnavailableError)
#         ),
#         before_sleep=before_sleep_log(logger, logging.WARNING),
#     )


@retry(wait=wait_fixed(3),  # 重试之前等待3秒
       stop=stop_after_delay(7) | stop_after_attempt(3),  # 同时满足用 | 没毛病：重试7秒重试3次
       retry_error_callback=lambda log: logger.error(log),
       reraise=True)
def request(url=None, json=None, parser=lambda x: x, encoding=None, **kwargs):
    """

    :param url:
    :param json:
    :param parser: None 的时候返回r，否则返回 parser(r.json())
    :param kwargs:
    :return:

        response = requests.request("GET", url, headers=headers, params=querystring)

    """
    method = 'post' if json is not None else 'get'  # 特殊情况除外
    logger.info(f"Request Method: {method}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE '
    }
    r = requests.request(method, url, json=json, headers=headers)
    r.encoding = encoding if encoding else r.apparent_encoding

    if parser is None:
        return r
    return parser(r.json())


def is_url_alive(url):
    request = requests.head(url)
    return True if request.status_code == 200 else False


if __name__ == '__main__':
    print(request4retry('xx'))