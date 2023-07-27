#!/usr/bin/env bash
# @Project      : MeUtils
# @Time         : 2022/7/7 上午11:20
# @Author       : yuanjie
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

ps -ef | grep python | awk '{print $2}' # pid