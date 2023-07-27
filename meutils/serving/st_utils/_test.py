#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : config
# @Time         : 2023/4/26 10:40
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.serving.st_utils import *

st.set_page_config(page_title='🔥ChatPDF', layout='wide', initial_sidebar_state='collapsed')


################################################################################################################
class Conf(BaseConfig):
    encode_model = 'nghuyong/ernie-3.0-nano-zh'
    llm = "THUDM/chatglm-6b"  # /Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm
    cachedir = 'pdf_cache'

    topk: int = 3
    threshold: float = 0.66


conf = Conf()
conf = set_config(conf)

if st.session_state.get('init'):
    st.json(st.session_state)
