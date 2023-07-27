#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : x
# @Time         : 2023/5/19 14:02
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from qdrant_client import QdrantClient
qdrant = QdrantClient("http://124.221.252.151:6333") # Connect to existing Qdrant instance, for production
qdrant.create_collection('test', vectors_config={})