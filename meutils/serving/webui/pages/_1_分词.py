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
from stopwords import filter_stopwords

from meutils.pipe import *
from meutils.ai_nlp.word_segmentation import WordSegmentation
from meutils.serving.st_utils import *

title = Path(__file__).stem.split('_')[-1]
st.set_page_config(title, page_icon='🔥', layout='wide', initial_sidebar_state='collapsed')
st.title(title)
hide_st_style('🔥DevelopedBy@数据科学研发中心-AI团队')

with st.form(title):
    text = """
    东北证券股份有限公司（以下简称“公司”）前身为吉林省证券有限责任公司。2000 年 6 月经中国证监会批准，经过增资扩股成立东北证券有限责任公司。
    """
    cols = st.columns(3)
    with cols[0]:
        option = st.selectbox('算法：', ('平衡模式', '快速模式', '精确模式'))
    with cols[1]:
        is_filter = st.selectbox('过滤停用词：', ('否', '是')) == '是'
    mode = {
        '平衡模式': 'base',
        '快速模式': 'fast',
        '精确模式': 'accurate'
    }.get(option, 'fast')
    nlp = WordSegmentation(mode)

    text = st.text_area("文本：", text.strip(), height=100)

    if st.form_submit_button('🚀开始计算'):
        with st.spinner('AI正在计算...'):
            ws = nlp([text])[0]
            if is_filter:
                ws = filter_stopwords(ws)

            annotations = []
            for i, w in enumerate(ws):
                if i % 2:
                    annotations.append(annotation(w, label='', color="blue"))
                else:
                    annotations.append(annotation(w, label='', color="black"))

            annotated_text(*annotations)
