#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : wechat
# @Time         : 2021/6/7 11:17 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://wechatpy.readthedocs.io/zh_CN/master/work/client.html

from meutils.pipe import *

from wechatpy.enterprise import WeChatClient as _WeChatClient


class WeChatClient(_WeChatClient):

    def __init__(self, corp_id, secret,
                 api_base_url=None,
                 agent_id=None,
                 access_token=None,
                 session=None, timeout=None, auto_retry=True, **kwargs):
        self.corp_id = corp_id
        self.secret = secret
        self.agent_id = agent_id
        self.API_BASE_URL = api_base_url if api_base_url else 'https://qyapi.weixin.qq.com/cgi-bin/'

        super().__init__(
            corp_id, secret, access_token, session, timeout, auto_retry
        )

    def fetch_access_token(self):
        return self._fetch_access_token(
            url=f'{self.API_BASE_URL}gettoken',
            params={
                'corpid': self.corp_id,
                'corpsecret': self.secret
            }
        )

    @staticmethod
    def name2id(name='AI小分队'):
        from meutils.hash_utils import murmurhash
        return murmurhash(name)


if __name__ == '__main__':
    # 公网测试
    corp_id = 'wwc18433f3075302e4'
    secret = 'iL_8JXBoB5vFITCcOk2-EvP6TcOnVCjZI1LRw8vidtE'
    agent_id = '1000002'
    api_base_url = None

    # 内外AI：
    corp_id = 'ww3c6024bb94ecef59'
    secret = 'empKNMx-RSgd4tK6uzVA56qCl1QY6eErRdSb7Hr5vyQ'
    agent_id = '1000041'
    api_base_url = 'https://qywxlocal.nesc.cn:7443/cgi-bin/'

    wc = WeChatClient(corp_id, secret, api_base_url)
    name = 'AI应用交流群'
    chat_id = wc.name2id(name)
    # wc.appchat.create(chat_id=chat_id, name=name, owner='YuanJie', user_list=['YuanJie', 'yayoYan'])
    # wc.appchat.create(chat_id=chat_id, name=name, owner=7683, user_list=[7683, 7559])

    # wc.appchat.create(chat_id=chat_id, name=name, owner=7683, user_list=[7683, 7689])
    # wc.appchat.send_text(chat_id, f"{name}#chat_id: {chat_id}")
    # wc.appchat.update(chat_id, add_user_list=[7838])
    # wc.appchat.send(chat_id, 'textcard', **{'title': 'Title', 'description': 'description', 'url': 'http://'})
    # wc.appchat.send_text(chat_id, '# 我是个机器人🤖')
    # wc.appchat.send(chat_id, 'markdown', content='# 我是个机器人🤖') # 不支持
