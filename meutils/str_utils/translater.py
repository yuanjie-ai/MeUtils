#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : translater
# @Time         : 2022/5/24 下午3:24
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


import hashlib
import hmac

from meutils.pipe import *

endpoint = "tmt.tencentcloudapi.com"
secret_id = "AKIDa9eDT1eYP5amxLnjme3KQrma6Vjp3gZM"
secret_key = "nlcNx68yc5QalkYBd1DmBPRIH9rNI3e3"


def get_string_to_sign(method, endpoint, params):
    s = method + endpoint + "/?"
    query_str = "&".join("%s=%s" % (k, params[k]) for k in sorted(params))
    return s + query_str


def sign_str(key, s, method):
    hmac_str = hmac.new(key.encode("utf8"), s.encode("utf8"), method).digest()
    return base64.b64encode(hmac_str)


@lru_cache()
def translater(q="苹果", fromLang='auto', toLang='en'):
    """
        for i in '业务条线、业务归口单位、业务负责人'.split('、'):
            to_hump(translater(i))
    @param q:
    @param fromLang:
    @param toLang:
    @return:
    """
    data = {
        'SourceText': q,
        'Source': fromLang,
        'Target': toLang,
        'Action': "TextTranslate",
        'Nonce': random.randint(32768, 65536),
        'ProjectId': 0,
        'Region': 'ap-hongkong',
        'SecretId': secret_id,
        'SignatureMethod': 'HmacSHA1',
        'Timestamp': int(time.time()),
        'Version': '2018-03-21',
    }
    s = get_string_to_sign("GET", endpoint, data)
    data["Signature"] = sign_str(secret_key, s, hashlib.sha1)

    # 此处会实际调用，成功后可能产生计费
    r = requests.get("https://" + endpoint, params=data, timeout=3)

    return r.json()['Response']['TargetText']


if __name__ == '__main__':
    print(translater())
    print(translater('apple', 'auto', 'zh'))
