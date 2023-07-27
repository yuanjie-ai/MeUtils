#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : todo
# @Time         : 2023/5/8 13:49
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from urllib.parse import urlparse

url = 'https://www.example.com/path/to/something?a=1&b=2#fragment'
parsed_url = urlparse(url)

print(parsed_url.scheme)  # https
print(parsed_url.netloc)  # www.example.com
print(parsed_url.path)  # /path/to/something
print(parsed_url.query)  # a=1&b=2
print(parsed_url.fragment)  # fragment
