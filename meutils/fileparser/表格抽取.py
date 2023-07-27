#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : 表格抽取
# @Time         : 2023/7/17 18:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import os
from dataclasses import dataclass
from typing import List
from collections import Counter

import pandas as pd
import pdfplumber
import tabulate


def extract_tables_with_text(pdf) -> List[str]:
    """抽取表格并嵌入文本"""

    def clean_cell_text(text):
        """
        清除文本中的换行符和多余空格
        """
        if text is None:
            return ""
        text = text.replace("\n", "")
        # 去除字符串开头和结尾的空白字符
        text = text.strip()
        return text

    def check_bboxes(word, table_bbox):
        left = word['x0'], word['top'], word['x1'], word['bottom']
        r = table_bbox
        return left[0] > r[0] and left[1] > r[1] and left[2] < r[2] and left[3] < r[3]

    def keep_visible_lines(obj):

        if obj['object_type'] == 'rect':
            return obj['non_stroking_color'] == 0
        return True

    lines = []
    page_counter = 0
    # 用来缓存没完整展示的表
    pending_table = []
    tp = None
    for page_number, page in enumerate(pdf.pages, start=0):
        p = page.filter(keep_visible_lines)
        combine_flag = len(pending_table) != 0
        page_counter = page_number
        tables = p.find_tables(
            table_settings={
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                # "explicit_vertical_lines": self.curves_to_edges(p.curves) + p.edges,
                # "explicit_horizontal_lines": self.curves_to_edges(p.curves) + p.edges,
            }
        )
        if len(tables) != 0:
            is_over_footer = p.chars[-1].get('y0') >= p.bbox[3] - p.find_tables()[-1].bbox[3]
        else:
            is_over_footer = False
        bboxes = [table.bbox for table in tables]
        tables = [{'table': i.extract(), 'top': i.bbox[1]} for i in tables]
        if is_over_footer:
            tp = pd.DataFrame(tables[-1]['table']).applymap(clean_cell_text)
            tables = tables[0:len(tables) - 1]
        non_table_words = [word for word in p.extract_words() if
                           not any([check_bboxes(word, table_bbox) for table_bbox in bboxes])]

        for cluster in pdfplumber.utils.cluster_objects(non_table_words + tables, 'top', tolerance=5):
            for c in cluster:
                if 'text' in c and c['text'] != str(page_number) and c['text'] != non_table_words[-1]:
                    lines.append("".join(c['text']))
                elif 'table' in c:
                    if combine_flag:
                        dt = pd.concat([pd.concat(pending_table, axis=0),
                                        pd.DataFrame(c['table']).applymap(clean_cell_text)], axis=0)
                        combine_flag = False
                        pending_table = []
                    else:
                        dt = pd.DataFrame(c['table']).applymap(clean_cell_text)
                    tb = tabulate.tabulate(dt, tablefmt="pipe", showindex=False, headers="keys")
                    lines.append(tb)
        if is_over_footer:
            pending_table.append(tp)
    content_counter = Counter(lines)
    return [word for word in content_counter if content_counter[word] != page_counter]


@dataclass
class Document:
    """文档结构"""
    text: List[str]
    source: str


def extract_text(filepath) -> Document:
    with pdfplumber.open(filepath) as pdf:
        text = extract_tables_with_text(pdf)
    return Document(text=text, source=os.path.basename(filepath))


if __name__ == '__main__':
    """
    pdfplumber==0.9.0
    tabulate[widechars]==0.9.0
    numpy==1.21.5
    pandas==2.0.3
    """
    doc = extract_text("/Users/betterme/Downloads/H2_AN202303301584686196_1.pdf")
    for line in doc.text:
        print(line)