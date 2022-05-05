#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : path_utils
# @Time         : 2020/11/12 11:39 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

import os
from pathlib import Path

get_module_path = lambda path, file=__file__: \
    os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(file), path))

get_resolve_path = lambda path, file=__file__: (Path(file).parent / Path(path)).resolve()

if __name__ == '__main__':
    print(os.getcwd())
    print(os.path.dirname(__file__))
