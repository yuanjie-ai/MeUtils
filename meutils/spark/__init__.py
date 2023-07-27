#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : __init__.py
# @Time         : 2021/3/5 11:29 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

import pyspark.sql.functions as F

from pyspark.sql import *
from pyspark.sql.types import *

spark = (
    SparkSession.builder
        .appName("Yuanjie")
        .config('log4j.rootCategory', "WARN")
        .enableHiveSupport()
        .getOrCreate()
)

logger.info(f"Spark Version: {spark.version}")
