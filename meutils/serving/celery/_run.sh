#!/usr/bin/env bash
# @Project      : AI @by PyCharm
# @Time         : 2023/8/4 11:21
# @Author       : betterme
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  :

celery -A meutils.serving.celery.tasks worker -l info
#celery -A tasks worker -l info
