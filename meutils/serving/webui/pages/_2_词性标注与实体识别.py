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
from meutils.pipe import disk_cache

from meutils.ai_nlp.ner import Ner
from meutils.serving.st_utils import *

title = Path(__file__).stem.split('_')[-1]
st.set_page_config(title, page_icon='🔥', layout='wide', initial_sidebar_state='collapsed')
st.title(title)

hide_st_style('🔥DevelopedBy@数据科学研发中心-AI团队')

with st.form(title):
    text = """
    东北证券股份有限公司（以下简称“公司”）前身为吉林省证券有限责任公司。2000年6月中国证监会批准，经过增资扩股成立东北证券有限责任公司。
    """
    container = st.container()
    cols = st.columns(3)
    with cols[0]:
        option = st.selectbox('算法：', ('快速模式', '精确模式'), index=1)
    with cols[1]:
        is_filter = st.selectbox('仅保留实体：', ('否', '是')) == '是'

    mode = {
        '平衡模式': 'base',
        '精确模式': 'accurate'
    }.get(option, 'fast')
    nlp = Ner(mode, entity_only=is_filter)

    text = st.text_area("文本", text.strip(), height=100)

    if st.form_submit_button('🚀开始计算'):
        with st.spinner('AI正在计算...'):
            text = nlp([text])[0]

            annotations = []
            for word, flag in text:
                annotations.append(annotation(word, label=flag, color="blue"))

            annotated_text(*annotations)
