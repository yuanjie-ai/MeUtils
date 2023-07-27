#!/usr/bin/env bash
# @Project      : MeUtils
# @Time         : 2021/4/15 1:28 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

export LC_ALL="en_US.utf8"
yum install -y epel-release python36
pip3 install -U --no-cache-dir -i https://mirror.baidu.com/pypi/simple meutils
pip3 install -U meutils
nohup mecli register-ip /push/ann/ips & #  --sleep-time 10