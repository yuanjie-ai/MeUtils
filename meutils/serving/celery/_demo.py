#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2023/8/4 14:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

r = requests.post('http://0.0.0.0:8899/celery/create', json={'method': '11', 'url': '666'})
print(r.json())

task_id = r.json()['task_id'] # '1819728d-26e3-4165-b33e-683a8b4777c9'
print(requests.get(f'http://0.0.0.0:8899/celery/get/{task_id}').json())