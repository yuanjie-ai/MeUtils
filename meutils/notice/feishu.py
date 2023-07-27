#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : feishu
# @Time         : 2021/1/20 6:04 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.zk_utils import get_zk_config


def send_feishu(title='TEST', text='', hook_url='logger'):
    hook_url = get_zk_config('/push/bot').get(hook_url, hook_url)
    requests.post(
        hook_url,
        json={"title": str(title), "text": f'{text} '},  # "msg_type": "html"
    )


if __name__ == '__main__':
    # todo：
    #   1. 支持富文本，集成miwork
    #   2. 回调
    send_feishu(hook_url='ann监控')
