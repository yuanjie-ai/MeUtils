#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : debug
# @Time         : 2021/2/8 2:15 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
with CronTab(True) as cron:

    job = cron.new('59 23 * * * mecli-cron update_from_file /push/crontab/c3-miui-bw-algo-train-task03')
    job.every(0)