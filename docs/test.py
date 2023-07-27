#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.  @by PyCharm
# @File         : test
# @Time         : 2023/4/14 09:35
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

import os
import sys
import time
import pathlib
import datetime

os.environ['main'] = __file__
os.environ['oo'] = '10'


def main():
    file = os.environ.get('main')
    # 获取文件的创建时间和修改时间
    create_time = os.path.getctime(file)
    modify_time = os.path.getmtime(file)

    # 将时间戳转化为字符串格式
    create_time_str = str(datetime.datetime.fromtimestamp(create_time))
    modify_time_str = str(datetime.datetime.fromtimestamp(modify_time))

    print(f"File created at: {create_time_str}")
    print(f"File last modified at: {modify_time_str}")
    if file:
        # expire_time = 30 * 24 * 60 * 60  # days
        expire_time = 15  # test
        print(__file__)
        print(datetime.datetime.fromtimestamp(time.time()))
        print(datetime.datetime.fromtimestamp(pathlib.Path(__file__).stat().st_ctime))
        print(datetime.datetime.fromtimestamp(pathlib.Path(__file__).stat().st_mtime))

        delta = time.time() - pathlib.Path(__file__).stat().st_ctime
        print(delta)
        if delta > expire_time:
            sys.exit()


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


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(10)
