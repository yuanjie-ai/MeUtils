#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : rm_pycache
# @Time         : 2021/9/4 下午2:34
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


def rm_files(dir_home='/Users/yuanjie/python_package', file='__pycache__'):
    ps = Path(dir_home).glob('*')
    for p in ps:
        if p.name == file:
            cmd = f"rm -rf {p.absolute()}"
            logger.info(cmd)
            os.system(cmd)

        elif p.is_dir():
            rm_files(p)
