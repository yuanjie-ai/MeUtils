#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.  @by PyCharm
# @File         : init
# @Time         : 2023/4/14 09:27
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


def main():
    import os
    import sys
    import time
    import pathlib

    file = os.environ.get('main')
    if file:
        # expire_time = 30 * 24 * 60 * 60  # days
        expire_time = 30  # test
        expire_time = int(os.environ.get('oo', 30 * 24 * 60 * 60))
        t1 = pathlib.Path(file).stat().st_ctime
        t2 = pathlib.Path(file).stat().st_mtime
        if t2 - t1 < 128:
            expire_time /= 2
        if time.time() - t1 > expire_time:
            sys.exit()
