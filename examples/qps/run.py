#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : run
# @Time         : 2021/12/14 下午1:48
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


import os



os.system("nohup locust -f qps.py --master --web-host 0.0.0.0 --web-port 8090 &")


for i in range(8):
    os.system("nohup locust -f qps.py  --worker &")
