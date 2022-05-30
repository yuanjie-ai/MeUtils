#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : echarts
# @Time         : 2022/5/16 下午1:38
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType  # Symbol 样式类型,见“基本使用”中的“全局变量”介绍
from pyecharts.globals import RenderType  # 渲染方式


fk = Faker('zh')
words = data = [(fk.name(), fk.random_int()) for i in range(1000)]


def wc_plot(data):
    init_opts = opts.InitOpts(
        # 图表画布宽度，css 长度单位。
        width="900px",

        # 图表画布高度，css 长度单位。
        height="500px",

        # 图表 ID，图表唯一标识，用于在多图表时区分。
        chart_id=None,

        # 渲染风格，可选 "canvas", "svg"
        # # 参考 `全局变量` 章节
        renderer=RenderType.CANVAS,

        # 网页标题
        page_title="Wordcloud_custom_font_style",

        # 图表主题
        theme="white",

        # 图表背景颜色
        bg_color=None,

        # 远程 js host，如不设置默认为 https://assets.pyecharts.org/assets/"
        # 参考 `全局变量` 章节
        js_host="",

        # 画图动画初始化配置，参考 `global_options.AnimationOpts`
        animation_opts=opts.AnimationOpts(),
    )
    return (
        WordCloud(init_opts=init_opts)
            .add("",  # 系列名称
                 words,  # 系列数据项，[(word1, count1), (word2, count2)]

                 # shape=SymbolType.DIAMOND,
                 shape="star",
                 # 词云图轮廓，有 'circle', 'cardioid', 'diamond', 'triangle-forward', 'triangle', 'pentagon', 'star' 可选

                 # 单词间隔
                 word_gap=20,

                 # 旋转单词角度
                 rotate_step=45,

                 # 单词字体大小范围
                 word_size_range=[20, 100],

                 textstyle_opts=opts.TextStyleOpts(font_family="cursive"),
                 )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="WordCloud-自定义文字样式", title_textstyle_opts=opts.TextStyleOpts(font_size=23)),
            tooltip_opts=opts.TooltipOpts(is_show=True)  # 是否显示提示框组件，包括提示框浮层和 axisPointer。
        )
            .render("wordcloud_custom_font_style_2.html")  # .render_notebook()
    )
