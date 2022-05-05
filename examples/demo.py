#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : demo
# @Time         : 2021/2/26 6:53 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.decorators import func

ff = lambda x: x



range(10) | xProcessPoolExecutor(func(ff)) | xlist



from prestool.Tool import Tool

print(tool.get_ip_by_url('https://www.baidu.com'))


import requests
response = requests.request("GET", url, headers=headers, params=querystring)
