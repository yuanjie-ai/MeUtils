#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : __init__.py
# @Time         : 2021/2/26 4:19 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


def to_compress(df: pd.DataFrame, filename, method='zip', archive_name='data.csv', index=False, **to_csv_kwargs):
    """

    @param df:
    @param method: mode is one of {{'infer', 'gzip', 'bz2', 'zip', 'xz', None}}
    @param archive_name:
    @return:
    """
    to_csv_kwargs['index'] = index
    to_csv_kwargs['compression'] = dict(method=method, archive_name=archive_name)
    df.to_csv(filename, **to_csv_kwargs)


def to_excel(df2name_list, path='filename.xlsx', to_excel_kwargs=None):
    """多个sheet写入数据

    :param df2name_list:
    :param to_excel_kwargs:
    :return:
    """
    if to_excel_kwargs is None:
        to_excel_kwargs = {}

    with timer("to_excel"):
        with pd.ExcelWriter(path) as writer:
            for df, sheet_name in df2name_list:
                df.to_excel(writer, sheet_name, **to_excel_kwargs)


if __name__ == '__main__':
    to_compress(pd.DataFrame([1,2]), 'demo.zip')

    print(pd.read_csv('demo.zip'))