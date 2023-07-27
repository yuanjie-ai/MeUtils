#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : subprocess_demo
# @Time         : 2021/1/20 10:38 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 


import subprocess
# 返回值输出
status, output = subprocess.getstatusoutput('cat /proc/cpuinfo')


subprocess.call('ls')  # 可以直接call()调用

'''
#也可以使用subprocess.Popen
p = subprocess.Popen('ls', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
  print(line)

'''


# scp: https://github.com/jbardin/scp.py