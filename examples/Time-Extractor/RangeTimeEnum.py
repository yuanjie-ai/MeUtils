#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @File    : RangeTimeEnum.py
# @Software: PyCharm



# 范围时间的默认时间点
class RangeTimeEnum():
    day_break = 3  # 黎明
    early_morning = 8  # 早
    morning = 10  # 上午
    noon = 12  # 中午、午间
    afternoon = 15  # 下午、午后
    evening = 18 # 傍晚
    night = 18  # 晚上
    lateNight = 20  # 晚、晚间
    midNight = 23  # 深夜


if __name__ == "__main__":
    print(RangeTimeEnum.afternoon)
