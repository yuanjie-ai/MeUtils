#!/usr/bin/env bash
# @Project      : AI @by PyCharm
# @Time         : 2023/7/27 08:52
# @Author       : betterme
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  :

celery -A celery_tasks worker -l info
