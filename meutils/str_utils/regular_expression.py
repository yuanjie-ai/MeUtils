#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : re_utils
# @Time         : 2022/5/12 下午2:03
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

zh = re.compile('[a-zA-Z\u4e00-\u9fa5]+')  # 中文 + 字母
