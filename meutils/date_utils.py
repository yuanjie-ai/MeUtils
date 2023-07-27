#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : date_utils
# @Time         : 2020/11/12 11:41 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 时间/日期模块

from meutils.common import *


# pd.datetime.now().timestamp() # pd.datetime.now(cst_tz).timestamp()# 时间戳相差8*3600
# pd.read_csv(parse_dates)


def date_difference(
        fmt='%Y-%m-%d %H:%M:%S',
        start_date=None,  # Union[datetime.datetime, str, int]
        **kwargs) -> str:
    """
    start_date: datetime.datetime.today()
    days: float = ...,
    seconds: float = ...,
    microseconds: float = ...,
    milliseconds: float = ...,
    minutes: float = ...,
    hours: float = ...,
    weeks
    """
    if start_date is None:
        start_date = datetime.datetime.now()

    if isinstance(start_date, (str, int)):
        start_date = datetime.datetime.strptime(str(start_date), fmt)

    date = start_date - datetime.timedelta(**kwargs)
    return date.strftime(fmt)


def timestamp2str(timestamp, fmt='%Y-%m-%d %H:%M:%S'):
    """
    t = pd.datetime.now().timestamp()
    ts = pd.Series([t]*10, name='t')

    # 时间戳 转 时间字符串
    ts = ts.map(timestamp2str) # 会有时区问题 %Y-%m-%d %H:%M:%S
    # 时间字符串 转 时间
    ts = ts.astype('datetime64[ns]') # 慢一些 pd.to_datetime(ts, errors='coerce', infer_datetime_format=True)
    ts.astype('datetime64')
    ts.astype(np.datetime64)
    # 时间 转 时间戳
    ts.map(lambda x: x.timestamp())

    # 快捷转换
    pd.to_datetime(time.time(), unit='s') # Timestamp('2021-03-18 04:26:37.819004774')

    t = pd.to_datetime('2021-04-17 23:59:59')
    t.timestamp()*1000

    :param timestamp: s
    :param fmt:
    :return:

    """
    return time.strftime(fmt, time.localtime(timestamp))


def get_nday_list(n):
    """获取过去 N 天的日期"""
    before_n_days = []
    for i in range(1, n + 1)[::-1]:
        before_n_days.append(str(datetime.date.today() - datetime.timedelta(days=i)))
    return before_n_days


def date_range(**kwargs):
    """生成一段时间区间内的日期"""
    return pd.date_range(**kwargs)


if __name__ == '__main__':
    print(date_difference(days=1))
    print(date_difference('%Y%m%d', days=1))
    print(date_difference('%Y%m%d', start_date=20210222, days=1))
    print(date_difference('%Y%m%d', days=2))
    print(date_difference(fmt='%Y%m%d', days=1))
    print(get_nday_list(30))

