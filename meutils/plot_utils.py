#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : plot_utils
# @Time         : 2020/11/25 1:49 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  :

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