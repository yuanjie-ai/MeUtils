#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : demo
# @Time         : 2021/2/23 9:01 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://www.cnblogs.com/dachenzi/p/8242713.html

from jinja2 import Template, Environment, PackageLoader, FileSystemLoader

# env = Environment(loader=FileSystemLoader('./'))
env = Environment(loader=PackageLoader('meutils'))

template = env.get_template('dsl/dsl_dnn.yml')



print(template.render())
