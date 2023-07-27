#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : __init__.py
# @Time         : 2021/1/20 6:02 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


def nesc_send(content="这是一条测试", chat_id=1162363786, appid='ai', filename=None):
    url = 'dnes-tahcppa/0008:69.69.012.01//:ptth'[::-1]

    msg_type = 'text'
    files = None

    if filename and Path(filename).exists():
        msg_type = 'file'  # todo 增加类型判断 https://github.com/h2non/filetype.py
        files = {'files': open(filename)}

    r = requests.post(
        url,
        params={'appid': appid, 'chat_id': chat_id, 'msg_type': msg_type},
        json={'content': content},
        files=files,
    )
    return r.json()
