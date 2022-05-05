#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : jinja_utils
# @Time         : 2021/3/26 11:47 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://zhuanlan.zhihu.com/p/152203801

import jinja2

# from jinja2 import Template, Environment, PackageLoader, FileSystemLoader

# from meutils.path_utils import *
# template_path = get_module_path('./templates')
# env = Environment(loader=FileSystemLoader(template_path))
jinja_env = jinja2.Environment(loader=jinja2.PackageLoader('meutils'))
template = jinja_env.get_('demo.j2')
print(template)
# template = jinja_env.get_template('dsl/dsl_dnn.yml')


