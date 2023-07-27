#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : opt
# @Time         : 2022/5/16 下午4:26
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


def pd_set_option():
    """https://mp.weixin.qq.com/s/C-p_oLmr6j1dkiFF-BQMDA"""
    pd.set_option('display.precision', 6)  # 小数精度6位
    pd.set_option("display.max_rows", 999)  # 最多显示行数
    pd.reset_option("display.max_rows")  # 重置
    pd.set_option('display.max_columns', 100)  # 最多显示列100
    pd.set_option('display.max_columns', None)  # 显示全部列
    pd.set_option('display.max_colwidth', 100)  # 列宽
    pd.reset_option('display.max_columns')  # 重置
    pd.set_option("expand_frame_repr", True)  # 折叠
    pd.set_option('display.float_format', '{:,.2f}'.format)  # 千分位
    pd.set_option('display.float_format', '{:.2f}%'.format)  # 百分比形式
    pd.set_option('display.float_format', '{:.2f}￥'.format)  # 特殊符号
    pd.options.plotting.backend = "plotly"  # 修改绘图
    pd.set_option("colheader_justify", "left")  # 列字段对齐方式
    pd.reset_option('all')  # 全部功能重置
