#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : import_utils
# @Time         : 2022/9/15 下午4:16
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


def import_mains(dir, pattern='*.py', filter_prefix=('__', '.')):  # todo: 优化
    """加载文件夹下的所有app（递归）, 入口函数都是main"""

    app_home = Path(sys_path_append(dir))
    n = app_home.parts.__len__()

    main_map = {}
    for p in app_home.rglob(pattern):
        if str.startswith(p.name, filter_prefix):  # 跳过 filter_prefix
            continue

        home_parts = p.parts[n:]
        module_name = '.'.join(home_parts).strip('.py')
        module = importlib.import_module(module_name)

        if hasattr(module, 'main'):  # 含有main入口函数的
            main_map[f'{app_home.stem}.{module_name}'] = getattr(module, 'main')

    return main_map
