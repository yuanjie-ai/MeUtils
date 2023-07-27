#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : json_jmespath
# @Time         : 2021/1/25 12:09 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : https://github.com/jmespath/jmespath.py
# https://www.cnblogs.com/denise1108/p/10265911.html
# 解析dict、json字符串


import jmespath

jmespath.search('foo.bar[*].name', {"foo": {"bar": [{"name": "one"}, {"name": "two"}]}})

jmespath.search('foo.*.name', {"foo": {"bar": {"name": "one"}, "baz": {"name": "two"}}})


expression = jmespath.compile('foo.bar')
print(expression.search({'foo': [{'bar': 'baz'}]}))


import jsonpath
