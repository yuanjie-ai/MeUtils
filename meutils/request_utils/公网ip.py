#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : 公网ip
# @Time         : 2022/4/29 上午11:22
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 公网ip


from urllib import request
import re


# 通过sohu公共ip库获取本机公网ip
def get():
    sohu_ip_url = 'http://txt.go.sohu.com/ip/soip'
    r = request.urlopen(sohu_ip_url)
    text = r.read().decode()
    result = re.findall(r'\d+.\d+.\d+.\d+', text)
    if result:
        return result[0]
    else:
        return None


if __name__ == "__main__":
    result = get()
    print(result)
