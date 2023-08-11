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
nozh = re.compile('[^a-zA-Z\u4e00-\u9fa5]+')  # 中文 + 字母


# re.sub(r'=(.+)', r'=123','s=xxxxx')


def get_parse_and_index(text, pattern):
    """
    text = 'The quick brown cat jumps over the lazy dog'
    get_parse_and_index(text, r'cat')
    """
    # 编译正则表达式模式
    regex = re.compile(pattern)

    # 使用re.finditer匹配文本并返回匹配对象迭代器
    matches = regex.finditer(text)

    # 遍历匹配对象迭代器，输出匹配项及其在文本中的位置
    for match in matches:  # 大数据
        yield match.start(), match.end(), match.group()

