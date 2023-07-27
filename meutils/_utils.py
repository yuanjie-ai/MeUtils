#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : py_utils
# @Time         : 2022/7/25 上午10:14
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 主要是些内建的数据结构，tuple/list/set/dict/string

import json
import base64


# bytes/string

def bytes2base64(bytes_data):
    return base64.b64encode(bytes_data).decode()


# 列表
def list_replace(l, mapping=None):
    if mapping is None:
        mapping = {}
    return [mapping.get(i, i) for i in l]  # [mapping[i] if i in mapping else i for i in l]


def list_difference(l1, l2):
    """列表差集，保持l1的顺序"""
    s = frozenset(l2)
    return [i for i in l1 if i not in s]


def list_intersection(l1, l2):
    """列表交集，保持l1的顺序"""

    s = frozenset(l2)
    return [i for i in l1 if i in s]


# padding

list4log = lambda ls: "\n\t" + "\n\t".join(ls)

# 字典
dict2json = bjson = lambda dic: json.dumps(dic, indent=4, ensure_ascii=False)
json2dict = lambda s: json.loads(s.replace("'", '"'))


def dic2obj(dic):
    class Kwargs:
        pass

    kwargs = Kwargs()
    kwargs.__dict__ = dic
    return kwargs


def dict_explode(dic: dict):
    """
        d = {'a': range(10), 'b': range(20)}
        [(k, i) for k, v in d.items() for i in v]

    :param dic:
    :return:
    """
    return [(k, i) for k, v in dic.items() for i in v]


def multidict_reverse(multidict):
    """

    :param multidict:
    :return: {'k': [1, 2]} => {1: 'k', 2: 'k'}
    """
    return [(i, k) for k, v in multidict.items() for i in v]


def dict_merge(dicts):
    """
        pd.DataFrame(dicts).to_dict('list')
    @param dicts:
    @return:
    """
    dic = {}
    for d in dicts:
        for k, v in d.items():
            dic.setdefault(k, []).append(v)
    return dic


