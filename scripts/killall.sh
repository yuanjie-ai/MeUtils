#!/usr/bin/env bash
# @Project      : MeUtils
# @Time         : 2022/7/11 下午5:23
# @Author       : yuanjie
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

ps -ef | grep ipykernel_launcher | awk '{print $2}' | xargs kill -9
