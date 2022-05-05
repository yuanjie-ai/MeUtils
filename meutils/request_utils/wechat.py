#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : wechat
# @Time         : 2021/5/26 3:50 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import wechatsogou

# 可配置参数

# 直连
ws_api = wechatsogou.WechatSogouAPI()


ws_api.search_gzh('南京航空航天大学') | xlist | xprint

