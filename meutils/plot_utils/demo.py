#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : demo
# @Time         : 2022/11/8 上午9:01
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


import matplotlib.pyplot as plt
import scikitplot as skplt
import kds

from sklearn.datasets import load_iris
from sklearn import tree

X, y = load_iris(return_X_y=True)
clf = tree.DecisionTreeClassifier(max_depth=4, random_state=3)
clf = clf.fit(X[:100], y[:100])

y_true = y[:100]
y_prob = clf.predict_proba(X[:100])


plt.style.use('seaborn')
fig, ax = plt.subplots(1, 2, figsize=(16, 6))

skplt.metrics.plot_roc(y_true, y_prob, ax=ax[0])
kds.metrics.plot_lift(y_true, y_prob[:, 1])

plt.show()
