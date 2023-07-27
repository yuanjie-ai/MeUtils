#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : 1_分词
# @Time         : 2023/5/21 17:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


import streamlit as st
from annotated_text import annotated_text, annotation

from meutils.pipe import *
from meutils.ai_nlp.ner import Ner
from meutils.serving.st_utils import *

title = Path(__file__).stem.split('_')[-1]
st.set_page_config(title, page_icon='🔥', layout='wide', initial_sidebar_state='collapsed')
st.title(title)

hide_st_style('🔥DevelopedBy@数据科学研发中心-AI团队')

with st.form(title):
    text = """
    东北证券股份有限公司（以下简称“公司”）前身为吉林省证券有限责任公司。2000 年 6 月经中国证监会批准，经过增资扩股成立东北证券有限责任公司。
    """
    container = st.container()
    cols = st.columns(3)
    with cols[0]:
        options = ('快速模式', '精确模式')
        option2mode = dict(zip(options, ['fast', 'accurate']))
        options = st.multiselect('算法：', options=options, default=options)

    with cols[1]:
        is_filter = st.selectbox('仅保留实体：', ('否', '是')) == '是'

    text = st.text_area("文本", text.strip(), height=100)
    if st.form_submit_button('开始切词'):
        for option in options:
            nlp = Ner(mode=option2mode.get(option), entity_only=is_filter)
            _  =nlp([text])[0]
            annotations = []
            for word, flag in _:
                annotations.append(annotation(word, label=flag, color="blue"))
            st.markdown(f'\n')
            st.markdown(option+':')
            annotated_text(*annotations)
