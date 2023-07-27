#!/usr/bin/env bash
# @Project      : MeUtils
# @Time         : 2021/12/14 下午3:44
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

ps ax | grep "locust" | grep -v grep | awk '{ print $1 }'
ps -e | grep -w "locust" | awk '{print $1}'  | xargs kill -9