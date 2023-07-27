#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : nesc.
# @File         : hegui
# @Time         : 2021/11/4 上午10:33
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

from urllib import parse
from docxtpl import DocxTemplate, RichText

from meutils.pipe import *
from meutils.str_utils import arabic2chinese
from meutils.date_utils import date_difference
from meutils.request_utils.crawler import Crawler


############################################################
def get_context(url, xpath_map, date, body_xpath="""//*[@class="Custom_UnionStyle"]//text()"""):
    c = Crawler(url)

    context = {}
    for idx, (title_, url_, date_) in enumerate(zip(*[c.xpath(v) for k, v in xpath_map.items()]), 1):
        if date_.strip() == date:
            url_ = parse.urljoin(url, url_)
            lines = Crawler(url_).xpath(body_xpath)
            context[f'{arabic2chinese(idx)[1]}、{title_}'] = ''.join(lines).strip()
    return context


# url = "http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd/"
# xpath_map = {
#     'titles': '//*[@id="myul"]/li[*]/a//text()',
#     'urls': '//*[@id="myul"]/li[*]//@href',
#     'dates': '//*[@id="myul"]/li[*]/span//text()'
# }

url = "http://www.csrc.gov.cn/pub/newsite/zxgx/jigbsdt/"
xpath_map = {
    'titles': '/html/body/div/div/div[5]/div[2]/div/div[2]/ul/li[*]/a//text()',
    'urls': '/html/body/div/div/div[5]/div[2]/div/div[2]/ul/li[*]/a//@href',
    'dates': '/html/body/div/div/div[5]/div[2]/div/div[2]/ul/li[*]/span//text()'
}
监管动态 = get_context(url, xpath_map, '2021-11-04')

url = "http://www.csrc.gov.cn/pub/newsite/zqjjjgjgb/thywwgcfxx/jgb_xzjgl/"
xpath_map = {
    'titles': '//*[@id="myul"]/li[*]/a//text()',
    'urls': '//*[@id="myul"]/li[*]/a//@href',
    'dates': '//*[@id="myul"]/li[*]/span//text()'
}
法律法规跟踪 = get_context(url, xpath_map, '2021-10-15')

############################################################
date = date_difference(fmt='%Y年%m月%d日')
year = date[:4]
context = {
    'year': year,
    'date': date,
    '监管动态': 监管动态,
    '法律法规跟踪': 法律法规跟踪,
}

doc = DocxTemplate('合规日报模板.docx')
doc.render(context)
doc.save('合规日报模板_.docx')



