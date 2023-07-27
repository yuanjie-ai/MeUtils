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

template = env.get_template('demo.j2')


class A:
    safe = 1

    def __init__(self, username):
        self.username = username


content = template.render(
    name='liuhao', age='18', country='China',
    A=A,
    users=['u1', 'u2', 'u3'],
    my_dict={'k': 'v'},
)

print(content)

with open('./demo.conf', 'w') as fp:
    fp.write(content)
