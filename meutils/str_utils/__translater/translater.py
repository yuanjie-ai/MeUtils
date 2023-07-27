#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'translate'
__author__ = 'JieYuan'
__mtime__ = '19-3-1'
"""
import requests
import random
import hashlib

"""可以通过docker增加并发
https://www.cnblogs.com/fanyang1/p/9414088.html
https://github.com/ssut/py-googletrans

https://github.com/openlabs/Microsoft-Translator-Python-API
https://github.com/cognitect/transit-python
"""
from .tencent import trans_tencent
from googletrans import Translator
from .youdao import trans_youdao

translator = Translator(service_urls=['translate.google.cn', 'translate.google.com'])


def trans_google(q='苹果', fromLang='auto', toLang='en'):
    """

    :param q:
    :param fromLang:
    :param toLang: zh
    :return:
    """
    url = "http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=%s&tl=%s" % (fromLang, toLang)
    try:
        r = requests.get(url, {'q': q}, timeout=3)
        text = r.json()['sentences'][0]['trans']
    except Exception as e:
        print(e)
        text = translator.translate(q, toLang, fromLang).text
    return text




if __name__ == '__main__':
    print(trans_tencent())
    print(trans_google('apple', 'en', 'zh'))
    # print(trans_baidu('apple', 'en', 'zh'))
