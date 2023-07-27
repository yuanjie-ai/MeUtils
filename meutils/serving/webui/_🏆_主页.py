#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : _🏆_主页.py
# @Time         : 2023/5/21 17:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.serving.st_utils import *

title = Path(__file__).stem.split('_')[-1]
st.set_page_config(title, page_icon='🔥', layout='wide', initial_sidebar_state='collapsed')
st.title(title)
hide_st_style('🔥DevelopedBy@数据科学研发中心-AI团队')
