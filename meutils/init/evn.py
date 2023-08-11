#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : evn
# @Time         : 2023/4/27 16:57
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

import os

# 环境变量配置
os.environ['JINA_HIDE_SURVEY'] = '1'
os.environ['TOKENIZERS_PARALLELISM'] = "true"
os.environ['MOMENTO_AUTH_TOKEN'] = 'eyJlbmRwb2ludCI6ImNlbGwtNC11cy13ZXN0LTItMS5wcm9kLmEubW9tZW50b2hxLmNvbSIsImFwaV9rZXkiOiJleUpoYkdjaU9pSklVekkxTmlKOS5leUp6ZFdJaU9pSXpNVE16TURNek1ETkFjWEV1WTI5dElpd2lkbVZ5SWpveExDSndJam9pUTBGQlBTSjkuSVRlX01ZRnBoVTBVb1I0SkdKOU92QXZ4dUJUOHBiQnpDWWlhZjlkZFYwdyJ9'

# LLM
os.environ['LLM_ROLE'] = '你扮演的角色是ChatLLM大模型，是由Betterme开发，基于ChatLLM-1000B模型训练的。'
os.environ['PROMPT_TEMPLATE'] = """
{role}
根据以下信息，简洁、专业地回答用户的问题。如果无法得到答案，请回复：“根据已知信息无法回答该问题”或“没有提供足够的信息”。请勿编造信息，答案必须使用中文。
已知信息：
{context}
问题：
{question}
""".strip() # Let's think step by step


# """
# {role}
# 请根据以下<>中的信息简洁、专业地回答问题。
# 信息：<{context}>
# 问题：{question}
# 如果无法从中得到答案，请回答“根据已知信息无法回答该问题”或“没有提供足够的信息”。请使用中文回答，不允许添加编造内容。
# """

# MODELSCOPE_CACHE
# PPNLP
if __name__ == '__main__':
    from pprint import pprint

    pprint(os.environ['PROMPT_TEMPLATE'])
