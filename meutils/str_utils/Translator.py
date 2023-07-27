#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : baidu
# @Time         : 2022/10/26 下午3:00
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.hash_utils import md5
from meutils.request_utils import request4retry


class Translator(object):

    def __init__(self, appid, secretKey):
        self.appid = appid
        self.secretKey = secretKey
        self.url = "http://api.fanyi.baidu.com/api/trans/vip/translate"

    @disk_cache(location='__translator_cache')
    def query(self, q='苹果', fromLang='auto', toLang='en'):
        salt = random.randint(32768, 65536)
        # 生成签名
        sign = md5(f"{self.appid}{q}{salt}{self.secretKey}")

        data = {
            "appid": self.appid,
            "q": q,
            "from": fromLang,
            "to": toLang,
            "salt": salt,
            "sign": sign,
        }

        r = request4retry(self.url, 'post', data=data)
        return r.get('trans_result')


if __name__ == '__main__':
    appid = '20190718000319131'  # 你的appid
    secretKey = '***'  # 你的密钥
    print(Translator(appid, secretKey).query('中国有很多很多人'))
