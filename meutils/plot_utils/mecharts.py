#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : mecharts
# @Time         : 2023/4/7 11:58
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from pyecharts import options as opts
from pyecharts.charts import Bar, WordCloud, HeatMap, Polar, Graph


class Chart(object):

    def __init__(self, width='1000px', height='400px', title='', render='notebook', jupyter_port=9955):
        self.init_opts = opts.InitOpts(width, height)
        self.title_opts = opts.TitleOpts(title=title)
        self.render = render  # .html
        if self.render == 'notebook':
            self.set_jupyter(jupyter_port)

    def graph(self, nodes, links, **kwargs):  # 共现网络
        """

        :param nodes: [{"name": "节点1", 'symbolSize': 32}] # opts.GraphNode
        :param links: [{"source": "节点1", "target": "节点2", "value": "关系", "symbolSize": "词频"}] # opts.GraphLink
        :return:
        """

        # 展示图表
        graph = Graph(self.init_opts)

        # graph.set_global_opts(visualmap_opts=opts.VisualMapOpts(max_=120))  # 根据节点的value值映射，最大120，因为有120回
        graph.add(
            nodes=nodes,
            links=links,
            series_name='',
            repulsion=256,
            # layout='force',
            # edge_length=[1, 100],
            # edge_label=opts.LabelOpts(is_show=False, position="middle", formatter="{c}"),
            # itemstyle_opts=opts.ItemStyleOpts(border_color='blue', opacity='0.9'),  # 节点样式设置
            # label_opts=opts.LabelOpts(is_show=True, position='inside', color='red')  # 节点标签（人物名称）设置
            **kwargs
        )
        return self.return_func(graph)

    def wordcloud(self, data_pair, shape='circle', **kwargs):
        """

        :param data_pair: [('周杰伦', 100)]
        :param shape: ['circle', 'cardioid', 'diamond', 'triangle-forward', 'triangle', 'pentagon', 'star']
        :param kwargs:
        :return:
        """
        if isinstance(data_pair, dict):
            data_pair = data_pair.items()

        wc = WordCloud(self.init_opts)
        wc.set_global_opts(
            title_opts=opts.TitleOpts(title='词云'),
            # visualmap_opts=opts.VisualMapOpts(),
            # tooltip_opts=opts.TooltipOpts(is_show=True)
        )
        wc.add(series_name='', data_pair=data_pair, shape=shape, **kwargs)
        return self.return_func(wc)

    def bar(self, xaxis_data, name2ydata, render='notebook', **kwargs):
        bar = Bar(init_opts=self.init_opts)
        bar.set_global_opts(title_opts=self.title_opts)
        bar.add_xaxis(xaxis_data)

        for name, ydata in name2ydata.items() if isinstance(name2ydata, dict) else name2ydata:
            bar.add_yaxis(name, ydata)

        return self.return_func(bar)

    def return_func(self, chart):
        render = self.render
        if render == 'notebook':
            return chart.render_notebook()
        elif render:
            return chart.render(render)  # html地址
        return chart

    @staticmethod
    def set_jupyter(port=9955):
        """插件教程 https://zhuanlan.zhihu.com/p/408166097?utm_id=0"""
        # 只需要在顶部声明 CurrentConfig.ONLINE_HOST 即可
        from pyecharts.globals import CurrentConfig, OnlineHostType

        # OnlineHostType.NOTEBOOK_HOST 默认值为 http://localhost:8888/nbextensions/assets/
        CurrentConfig.ONLINE_HOST = OnlineHostType.NOTEBOOK_HOST.replace('8888', str(port))
