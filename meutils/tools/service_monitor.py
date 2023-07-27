#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : __init__.py
# @Time         : 2021/1/31 10:20 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : python meutils/clis/__init__.py

from meutils.pipe import *
from meutils.request_utils import request4retry

from itertools import zip_longest


class Item(BaseModel):
    name = 'name'
    url = ""
    get_data: list = []
    post_data: list = []
    keywords: list = []  # 判断词


class Items(BaseConfig):
    item_list: List[Item]


def monitor_task(item: Item):
    method = 'post' if item.post_data else 'get'
    flags = []
    for get_data, post_data in zip_longest(item.get_data, item.post_data):
        r = request4retry(item.url, method, return_json=False, params=get_data, json=post_data, timeout=3) # 8.0
        if r is None:
            flag = False
        else:
            flag = any(key in r.text for key in item.keywords)
        flags.append(flag)

    return (item.name, any(flags))


def main(filename):
    items = Items.parse_yaml(filename)
    return list(map(monitor_task, items.item_list))


if __name__ == '__main__':
    FILE_NAME = 'monitor.yml'
    print(main(FILE_NAME))
