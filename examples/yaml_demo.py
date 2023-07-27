#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : yaml_demo
# @Time         : 2021/1/29 11:07 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


print(yaml_load('conf.yaml'))

# print(eval(yaml_load('conf.yaml')['f'])(6666))
