#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : __init__.py
# @Time         : 2021/2/26 4:19 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
from zipfile import ZipFile

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


@timer("to_excel4dfs")
def to_excel4dfs(df2name_list, path='filename.xlsx', to_excel_kwargs=None):
    """多个sheet写入数据

    :param df2name_list:
    :param to_excel_kwargs:
    :return:
    """
    if to_excel_kwargs is None:
        to_excel_kwargs = {}

    with pd.ExcelWriter(path) as writer:
        for df, sheet_name in df2name_list:
            df.to_excel(writer, sheet_name, **to_excel_kwargs)


def read2write(input_file, output_file, func, batchsize=10e5):
    dfs = pd.read_csv(input_file, sep='\n', chunksize=batchsize, header=None)  # reader

    for df in tqdm(dfs):
        df = func(df)
        df.to_csv(output_file, header=False, index=False, mode='a')  # writer

    # todo 多进程，合并文件， os.getpid() + 时间戳 确定唯一文件


def zipfiles(files, out_file='file.zip', compression=0):
    """
    0 ZIP_STORED：不进行压缩，直接存储
    8 ZIP_DEFLATED：使用DEFLATE算法进行压缩，压缩率较高
    12 ZIP_BZIP2：使用BZIP2算法进行压缩，在某些情况下比DEFLATE更优秀
    14 ZIP_LZMA：使用LZMA算法进行压缩，压缩率最高
    """
    with ZipFile(out_file, compression=compression, mode='w') as f:
        for file in files:
            f.write(file)

    return out_file


if __name__ == '__main__':
    to_compress(pd.DataFrame([1, 2]), 'demo.zip')

    print(pd.read_csv('demo.zip'))
