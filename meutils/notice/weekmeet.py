#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : wechat
# @Time         : 2021/6/7 11:17 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
import time

from meutils.pipe import *
from meutils.notice.wechat import Bot

bot = Bot("5f51e925-1257-4f90-88ea-f474bc1e2a05")

json = {
    "msgtype": "news",
    "news": {
        "articles": [
            {
                "title": "数据科学研发中心周会",  # 14个字换行
                "description": "同学们，点击图片进教室，迟到发红包",  # 17个字换行
                "url": "https://meeting.tencent.com/s/UJ5c5nOdCJI3",
                "picurl": "https://i.loli.net/2021/08/03/CJeHpGuWXKrPgc3.jpg",  # 1068*455 150*150
            },
        ]
    }
}
logger.info("周会通知")
bot.send(json)

time.sleep(60 * 15)
json = {
    "msgtype": "text",
    "text": {
        "mentioned_mobile_list": ["@all"],
        "content": "点击图片进教室，周会已经开始啦",
    }
}
logger.info("周会开始")
bot.send(json)
