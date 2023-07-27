#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : doc
# @Time         : 2023/3/27 12:02
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


def doc2text(p):
    p = Path(p)
    import docx
    doc = docx.Document(p)
    text = ''
    for part in doc.paragraphs:
        _ = part.text.strip()
        if _:
            text += '\n' + _

    return p.parent.name, p.name, text.strip()
