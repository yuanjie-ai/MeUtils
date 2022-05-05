#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : qps
# @Time         : 2021/12/14 上午10:16
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://www.cnblogs.com/shenh/p/12424990.html


from locust import HttpUser, TaskSet, task, between

from meutils.pipe import *


class Tasks(TaskSet):

    @task
    def post(self):
        r = self.client.post(
            "/cess-online-6/function-pipeline/v1/engine/cess-online-6/pipeline/default/execution",
            json={"request": {"userId": "18550288233"}},
            timeout=2000
        )
        _ = r.json()
    # @task
    # def get(self):
    #     _ = self.client.get("/").text


class WebUser(HttpUser):
    host = "http://192.18.27.124:30000"
    tasks = [Tasks]

    min_wait = 3000  # 单位为毫秒
    max_wait = 6000  # 单位为毫秒
    wait_time = between(0, 3)

# if __name__ == "__main__":
#     import os
#
#     os.system("locust -f qps.py --host=https://www.cnblogs.com")
