#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : dict2yaml
# @Time         : 2021/2/5 3:39 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

d = {'a': 1, 'b': [1, 2], 'c': {'cc': 1}, 'd': [[1, 2], [3, 4]]}

print(yaml.dump(d))

yaml.dump(d, stream=open('dict2yaml.yaml', 'w'))

print(yaml_load('dict2yaml.yaml'))

def dict2yaml(dic, file=None):
    s = yaml.dump(dic)
    print(s)

    if file:
        with open(file, 'w') as f:
            f.write(s)


dict2yaml(d, 'xx.yaml')
