#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : str_utils
# @Time         : 2020/11/12 1:48 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 
from meutils.pipe import *
from meutils.request_utils.crawler import Crawler

"""todo
url 拼接

"""


def str_replace(s: str, dic: dict):
    """多值替换
        str_replace('abcd', {'a': '8', 'd': '88'})
    """
    return s.translate(str.maketrans(dic))


def unquote(s='%E6%9C%80%E6%96%B0%E6%9C%8D%E5%8A%A1'):
    """http字符串解码"""
    from urllib import parse

    return parse.unquote(s)


@lru_cache()
def arabic2chinese(arabic=123):
    c = Crawler(f'https://szjrzzwdxje.bmcx.com/{arabic}__szjrzzwdxje')
    return c.xpath('//span//text()')[-3:-1]


if __name__ == '__main__':
    print(str_replace('abcd', {'a': '8', 'd': '88'}))
    print(unquote())
    print(arabic2chinese())
