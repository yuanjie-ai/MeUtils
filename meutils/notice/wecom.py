#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : wecom
# @Time         : 2021/8/31 下午5:16
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://github.com/quanttide/wecom-sdk-py/tree/master/wechatwork_sdk


from meutils.pipe import *
from meutils.hash_utils import *


class Article(BaseConfig):
    title: str = '百度热榜'
    description: str = '百度热榜'
    url: str = 'https://top.baidu.com/board?tab=realtime'
    picurl: str = 'http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png'


class Wecom(object):

    def __init__(self, hook_url=None):
        self.hook_url = self._convert_hook_url(hook_url)

    def send_markdown(self, title="", content=""):

        if isinstance(content, (list, tuple)):
            content = '\n'.join(content).strip()

        json = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"# {title}\n{content}".strip()
            }
        }
        return self._send(json)

    def send_text(self, title="", content="", mentioned_mobile_list=None):
        json = {
            "msgtype": "text",
            "text": {
                "content": f"{title}\n{content}".strip()
            }
        }
        if mentioned_mobile_list:  # "@all"'
            json['text']['mentioned_mobile_list'] = mentioned_mobile_list

        return self._send(json)

    def send_news(self, articles: Union[Article, List[Article]]):
        """
        json = {
        "msgtype": "news",
        "news": {
        "articles": [
            {
                "title": "中秋节礼品领取1",
                "description": "今年中秋节公司有豪礼相送",  # 多条不会显示
                "url": "www.qq.com",
                "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
            }
        ]}}
        """
        json = {
            "msgtype": "news",
            "news": {
                "articles": []
            }
        }
        if isinstance(articles, Article):
            articles = [articles]

        for article in articles:
            json["news"]["articles"].append(article.dict())
        return self._send(json)

    def send_card(self, ):
        json = {
            "msgtype": "template_card",
            "template_card": {
                "card_type": "news_notice",
                "source": {
                    "icon_url": "https://wework.qpic.cn/wwpic/252813_jOfDHtcISzuodLa_1629280209/0",
                    "desc": "企业微信"
                },
                "main_title": {
                    "title": "欢迎使用企业微信",
                    "desc": "您的好友正在邀请您加入企业微信"
                },
                "card_image": {
                    "url": "https://wework.qpic.cn/wwpic/354393_4zpkKXd7SrGMvfg_1629280616/0",
                    "aspect_ratio": 2.25
                },
                "vertical_content_list": [
                    {
                        "title": "惊喜红包等你来拿",
                        "desc": "下载企业微信还能抢红包！"
                    }
                ],
                "horizontal_content_list": [
                    {
                        "keyname": "邀请人",
                        "value": "张三"
                    },
                    {
                        "keyname": "企微官网",
                        "value": "点击访问",
                        "type": 1,
                        "url": "https://work.weixin.qq.com/?from=openApi"
                    },
                    {
                        "keyname": "企微下载",
                        "value": "企业微信.apk",
                        "type": 2,
                        "media_id": "MEDIAID"
                    }
                ],
                "jump_list": [
                    {
                        "type": 1,
                        "url": "https://work.weixin.qq.com/?from=openApi",
                        "title": "企业微信官网"
                    },
                    {
                        "type": 2,
                        "appid": "APPID",
                        "pagepath": "PAGEPATH",
                        "title": "跳转小程序"
                    }
                ],
                "card_action": {
                    "type": 1,
                    "url": "https://work.weixin.qq.com/?from=openApi",
                    "appid": "APPID",
                    "pagepath": "PAGEPATH"
                }
            }
        }

        self._send(json)

    def send_image(self, path='http://www.nesc.cn/dbzq/images/logo.png'):
        bytes_data = self._get_bytes(path)
        body = {
            "msgtype": "image",
            "image": {
                "base64": bytes2base64(bytes_data),
                "md5": md5(bytes_data, False)
            }
        }
        return self._send(body)

    def send_file(self, path, type='file'):
        """

        @param path:
        @param type: 要求文件大小在5B~20M之间，媒体文件类型，分别有图片（image）、语音（voice）、视频（video），普通文件(file)
        @return:
        """

        upload_media_url = f"""{self.hook_url.replace('send?', 'upload_media?')}&type={type}"""

        # bytes_data = self._get_bytes(path)
        # files = {'data': bytes_data} # 这样文件名为data

        with open(path, 'rb') as f:
            files = {'data': f}
            response = requests.post(upload_media_url, files=files)
        try:
            media_id = response.json()['media_id']
            body = {"msgtype": type, type: {"media_id": media_id}}
            return self._send(body)

        except Exception as e:
            return response.json()

    def _send(self, body=None):
        if body is None:
            body = {
                "msgtype": "text",
                "text": {
                    "content": "南京今日天气：29度，大部分多云，降雨概率：60%",
                    "mentioned_mobile_list": ["18550288233", "@all"]
                }
            }
        return requests.post(url=self.hook_url, json=body)

    @staticmethod
    def _get_bytes(path):
        if path.startswith('http'):
            bytes_data = requests.get(path).content
        else:
            bytes_data = Path(path).read_bytes()
        return bytes_data

    @staticmethod
    def _convert_hook_url(hook_url):
        if hook_url is None or hook_url == '':
            hook_url = '43e28f3b-0c07-492c-aa37-a59abc3acf43'

        if not hook_url.startswith('http'):
            hook_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={hook_url}'
        return hook_url


if __name__ == '__main__':
    wecom = Wecom()
    # wecom.send_news(Article())
    # wecom.send_file('wecom.py')
    wecom.send_card()
