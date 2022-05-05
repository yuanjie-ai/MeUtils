# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : app_run
# @Time         : 2020/11/5 4:48 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : https://github.com/google/python-fire/blob/master/docs/guide.md
"""
'console_scripts': [
    'app-run=appzoo.app_run:cli'
]
"""
from meutils.pipe import *


class CLIRun(object):
    """doc"""

    def __init__(self, **kwargs):
        pass

    def apps_list(self, apps='apps'):
        """
        apps/apps_streamlit
        """

    def pip(self, *packages):
        """
            mecli - pip "meutils appzoo"
        :param packages:
        :return:
        """
        packages = " ".join(packages)
        cmd = f"pip install -U --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple {packages} && pip install -U {packages}"
        logger.info(cmd)
        os.system(cmd)
        # todo: 增加常用包更新


def cli():
    fire.Fire(CLIRun)


if __name__ == '__main__':
    print(CLIRun().pip())


#
# import fire
#
# def add(x, y):
#   return x + y
#
# def multiply(x, y):
#   return x * y
#
# if __name__ == '__main__':
#   fire.Fire()
# We can use this like so:
#
# $ python example.py add 10 20
# 30
# $ python example.py multiply 10 20
# 200