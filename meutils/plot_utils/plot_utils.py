#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : plot_utils
# @Time         : 2020/11/25 1:49 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : https://blog.csdn.net/hiroyuu008/article/details/122013763

from meutils.pipe import *
import seaborn as sns

sns.set(style="darkgrid")  # darkgrid, whitegrid, dark, white,和ticks
sns.set_context('paper')


# sns.plotting_context()
# sns.axes_style()
# plt.style.use('ggplot')
# plt.style.use('seaborn')

def plot_cum_cr(s: pd.Series, bin_wide=100, bins=12, name=None):
    """Conversion rate
    累积转化率
    """
    l = []
    for i in range(1, bins + 1):
        l.append(s[:i * bin_wide].mean())

    pd.Series(l).to_frame(name).plot(marker='.', linestyle='-')
    return l

# https://www.cnblogs.com/Yang-Sen/p/11226005.html
# import cufflinks as cf
# cf.set_config_file(offline=True)



import random
from pyecharts import charts


class WordCloud(object):

    def __init__(self, data_pair, shape=None, width='900px', height='500px'):
        """
        ['circle', 'cardioid', 'diamond', 'triangle-forward', 'triangle', 'pentagon', 'star']
        wc.render()
        wc.render_notebook()

        """
        self._shapes = ['circle', 'cardioid', 'diamond', 'triangle-forward', 'triangle', 'pentagon', 'star']
        self.data_pair = data_pair
        self.shape = shape if shape else random.choice(self._shapes)
        self.width = width
        self.height = height

    @property
    def wc(self):
        wc = charts.WordCloud()
        wc.add("WordCloud", data_pair=self.data_pair, shape=self.shape)
        wc.width = self.width
        wc.height = self.height
        return wc


if __name__ == '__main__':
    pairs = [('中国', 33),
             ('苹果', 24),
             ('奚梦瑶', 20),
             ('美国', 16),
             ('特朗普', 16),
             ('何猷君', 15),
             ('戛纳', 13),
             ('红毯', 12),
             ('iPhone', 12),
             ('车队', 9),
             ('车祸', 9),
             ('优衣', 9),
             ('信息', 9),
             ('李亚鹏', 9),
             ('恋情', 9),
             ('任素', 9),
             ('男孩', 9),
             ('亚洲', 8),
             ('孩子', 8),
             ('大学生', 8)]

    WordCloud(pairs).wc.render_notebook()
    WordCloud(pairs).wc.render('x.html')


