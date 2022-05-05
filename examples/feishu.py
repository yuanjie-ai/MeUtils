#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : feishu
# @Time         : 2021/4/18 11:46 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.notice.feishu import send_feishu
from meutils.pd_utils import df2bhtml
import pandas as pd
send_feishu(text=df2bhtml(pd.DataFrame(range(10))))
