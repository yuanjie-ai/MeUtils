#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : shell_utils
# @Time         : 2021/1/19 8:07 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


def wget(url, rename=None, is_return=False):
    cmd = f"wget {url}"
    if rename:
        cmd += f" -O {rename}"


if __name__ == '__main__':
    print(Path('xx') / '/x/xx/xxxx')
