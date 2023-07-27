#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : 1_分词
# @Time         : 2023/5/21 17:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

import pandas as pd
import streamlit
from annotated_text import annotated_text, annotation
from sentence_transformers import SentenceTransformer

from meutils.pipe import *
from meutils.serving.st_utils import *

title = Path(__file__).stem.split('_')[-1]
st.set_page_config(title, page_icon='🔥', layout='wide', initial_sidebar_state='collapsed')
st.title(title)

hide_st_style('🔥DevelopedBy@数据科学研发中心-AI团队')

SentenceTransformer = lru_cache(SentenceTransformer)


def nlp(text_pair, model='shibing624/text2vec-base-chinese'):
    cache_folder = None
    if Path('/data/MODEL/huggingface').is_dir():
        cache_folder = '/data/MODEL/huggingface'
    embeddings = (
        SentenceTransformer(model, cache_folder=cache_folder)
        .encode(text_pair, normalize_embeddings=True)
    )
    _ = [{'文本1': text_pair[0], '文本2': text_pair[1], '相似度': (embeddings[0] * embeddings[1]).sum()}]
    return pd.DataFrame(_)


nlp = disk_cache(nlp, 'cachedir_sim')

with st.form(title):
    text1 = """
    《东北证券股份有限公司信息技术管理制度》第六条 公司经理层负责落实信息技术管理目标，对信息技术管理工作承担责任，履行下列职责：
（一）组织实施董事会相关决议；
（二）建立责任明确、程序清晰的信息技术管理组织架构，明确管理职责、工作程序和协调机制；
（三）完善绩效考核和责任追究机制；
（四）公司章程规定或董事会授权的其他信息技术管理职责。
    """
    text2 = """
    第八条 证券基金经营机构经营管理层负责落实信息技术管理目标，对信息技术管理工作承担责任，履行下列职责：    
    """

    cols = st.columns(3)
    with cols[0]:
        option = st.selectbox('算法：', ('shibing624/text2vec-base-chinese', 'GanymedeNil/text2vec-large-chinese'))

    text1 = st.text_area("文本1：", text1.strip(), height=120)
    text2 = st.text_area("文本2：", text2.strip(), height=120)

    if st.form_submit_button('🚀开始计算'):
        with st.spinner('AI正在计算...'):
            st.dataframe(nlp([text1, text2], option))
