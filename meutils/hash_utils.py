#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : DeepNN.
# @File         : hashtrick
# @Time         : 2020-04-10 16:54
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

import hashlib as _hashlib
from functools import lru_cache
from sklearn.utils.murmurhash import murmurhash3_32 as _murmurhash3_32

# ME
from meutils.decorators import singleton

"""Java
import java.nio.charset.StandardCharsets
import com.google.common.hash.Hashing.murmur3_32

def hash(key: String = "key", value: String = "value", bins: Int = 10000): Int = {
    val hashValue: Int = murmur3_32.newHasher.putString(f"{key}:{value}", StandardCharsets.UTF_8).hash.asInt
    Math.abs(hashValue) % bins  
  }
"""


def md5(string: str, encoding=True):
    s = string.encode('utf8') if encoding else string
    return _hashlib.md5(s).hexdigest()


def murmurhash(key="key", value="value", bins=None, str2md5=True):
    """key:value"""
    string = f"{value}:{key}"
    if str2md5:
        string = md5(string)

    _ = _murmurhash3_32(string, positive=True)  # 与java一致
    return _ % bins if bins else _


@lru_cache()
class ABTest(object):
    """
    https://abtestguide.com/calc/
    http://www.abtestcalculator.com/
    https://zhuanlan.zhihu.com/p/130778873
    https://blog.csdn.net/qq_43656500/article/details/120977558
    https://blog.csdn.net/weixin_43885654/article/details/106750764

    expid = '10001'
    r = {'expid': expid}

    if ABTest((0, 99), **r).is_hit('id'):
        r['data'] = ...
    elif ABTest((100, 199), **r).is_hit('id'):
        r['data'] = ...
    """

    def __init__(self, expid='10001', ranger=(0, 9), bins=100):
        self._bins = bins
        self._ranger = set(range(*ranger))  # 控制流量
        self._expid = expid

    @lru_cache(8 * 10240)  # 8 * 20kb * 长度
    def is_hit(self, value="userid"):
        s = f"{value}:{self._expid}"

        _ = _murmurhash3_32(s, positive=True) % self._bins  # 与java一致
        return _ in self._ranger


if __name__ == '__main__':
    print(md5("key:value"))
    print(murmurhash(str2md5=False, bins=10000))  # 3788
    print(murmurhash(str2md5=True, bins=10000))  # 1688 5608
    expid = '10001'
    r = {'expid': expid}

    print(ABTest(**r, ranger=(0, 99)).is_hit('id'))
    r = {'expid': 'expid'}

    print(ABTest(**r, ranger=(0, 99)).is_hit('id'))
