#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : asr
# @Time         : 2023/5/17 13:51
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.str_utils import chinese_convert

from faster_whisper import WhisperModel


model = WhisperModel(model_size_or_path='large-v2', device="cpu")
segments, info = model.transcribe(
    "../../../zh_.wav",
    beam_size=5,
    # language='en'
)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, chinese_convert(segment.text)))
