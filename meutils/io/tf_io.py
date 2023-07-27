#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : tf_io
# @Time         : 2021/2/26 4:19 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://www.jianshu.com/p/c2fabc8a6dad
"""
tf 不支持Path
Path('hdfs://')会丢失一个/
"""

import tensorflow as tf

from meutils.pipe import *
from meutils.pd_utils import split as df_split
from meutils.path_utils import get_module_path
from meutils.date_utils import date_difference
from meutils.decorators.retry import wait_retry

HDFS = 'hdfs://easyops-cluster'
DATA = get_module_path("../data", __file__)
OUTPUT = "OUTPUT"
_FLAG = f"{DATA}/_FLAG"
_SUCCESS = f"{DATA}/_SUCCESS"


def get_lastest_path(path, max_tries=8, threshold=1):
    for i in range(max_tries):
        date = date_difference('%Y%m%d', days=i)
        path_ = f"{path}{date}"
        if tf.io.gfile.exists(path_):
            files = tf.io.gfile.glob(f"{path_}/*")
            if len(files) > 0 and tf.io.gfile.stat(files[0]).length // 1024 >= threshold:
                logger.info(path_)
                return path_
    logger.warning("无效路径")


def _process_hdfs_path(p):
    if p.startswith('/user/'):
        p = HDFS + p
    return p


def _process_pattern(pattern):
    pattern = _process_hdfs_path(pattern)

    if tf.io.gfile.isdir(pattern):  # 如果是个文件夹，默认匹配所有文件
        pattern = pattern + '/*'
    return pattern


def check_path(path):
    """判断文件文件夹是否存在"""
    path = _process_hdfs_path(path)
    return tf.io.gfile.exists(path)


@wait_retry(600)  # 10分钟check一次
def check_path_wait(path):
    return check_path(path)


def if_not_exist_makedir(path):
    path = _process_hdfs_path(path)
    if not tf.io.gfile.exists(path):
        logger.warning(f"{path} Does Not Exist, Make Dir")
        tf.io.gfile.makedirs(path)
    return path


def make_flag(output_dir, flag=_FLAG):
    output_dir = if_not_exist_makedir(output_dir)
    tf.io.gfile.copy(flag, f"{output_dir}/{Path(flag).name}", True)


def process_success(output_dir):
    make_flag(output_dir, _SUCCESS)


def rename(src, dst, overwrite=True):
    """支持文件and文件夹"""
    src = _process_hdfs_path(src)
    dst = _process_hdfs_path(dst)

    if not check_path(src):
        logger.error(f"{src}; No such file or directory")
        return

    tf.io.gfile.rename(src, dst, overwrite=overwrite)


def rm(path):
    path = _process_hdfs_path(path)

    if tf.io.gfile.isdir(path):
        tf.io.gfile.rmtree(path)
    elif tf.io.gfile.exists(path):  # 文件夹也返回 True
        tf.io.gfile.remove(path)


def cp(pattern, output_dir=DATA, with_success=True, filter_fn=None):
    """复制文件夹下的文件到新文件夹"""
    pattern = _process_pattern(pattern)
    output_dir = if_not_exist_makedir(output_dir)

    # 过滤文件夹、空文件、自定义过滤条件等
    files = []
    for file in tf.io.gfile.glob(pattern):
        if tf.io.gfile.isdir(file) or tf.io.gfile.stat(file).length == 0:  # Path(p).stat().st_size:
            continue
        files.append(file)

    if filter_fn is not None:
        files = list(filter(filter_fn, files))

    logger.debug("FILES:\n\t{}".format('\n\t'.join(files)))  # f"{}"里不支持 /

    # 复制
    def func(file):
        new_file = f"{output_dir}/{Path(file).name}"
        tf.io.gfile.copy(file, new_file, True)
        return new_file

    new_files = files | xThreadPoolExecutor(func, 16) | xlist  # 多线程，多进程如何？

    # 结束标识
    if with_success and output_dir.startswith("hdfs"):
        process_success(output_dir)

    return new_files


def df2write(df, file, num_partitions=1, sep='\t', index=False, header=False, with_success=True, **kwargs):
    """仅支持单文件，支持多线程写入
    写的时候不支持多个字符分割："delimiter" must be a 1-character string: 非逗号分割的提前合并
    """
    file = _process_hdfs_path(file)
    name = Path(file).name  # dir = file[::-1].split('/', 1)[1][::-1]
    dir = Path(file).parent.__str__().replace('hdfs:/', 'hdfs://')

    if_not_exist_makedir(str(dir))

    if num_partitions == 1:
        with tf.io.gfile.GFile(file, 'w') as f:
            df.to_csv(f, index=index, header=header, sep=sep, **kwargs)
            f.flush()
    else:

        logger.debug(f"ThreadPoolExecutor: part__*__{name}")

        def writer(args):
            idx, df = args
            file = f"{dir}/part__{idx}__{name}"

            with tf.io.gfile.GFile(file, 'w') as f:
                df.to_csv(f, index=index, header=header, sep=sep, **kwargs)
                f.flush()

        enumerate(df_split(df, num_partitions)) | xThreadPoolExecutor(writer, num_partitions)  # 加速不明显

    if with_success:
        process_success(dir)

    del df
    gc.collect()


def read2df(file, **kwargs):
    """仅支持单文件, 与pandas有些不兼容
    sep: 本地文件支持多字符作为分隔符，HDFS文件好像不支持
    pd.read_csv(p, iterator=True, chunksize=10000)
    """
    file = _process_hdfs_path(file)

    with tf.io.gfile.GFile(file, 'r') as f:  # todo: 中文异常
        return pd.read_csv(f, **kwargs)


def read2dataset(pattern, fmt='TextLineDataset', num_parallel_reads=1):
    """支持多文件大数据

    :param pattern:
    :param format: 'TextLineDataset', 'TFRecordDataset'
    :return:
        df = pd.DataFrame(map(bytes.decode, ds.as_numpy_iterator()))
        df = pd.DataFrame(map(lambda r: r.decode().split('____'), ds.as_numpy_iterator()), columns=['itemid', 'title'])
        for i in ds:
            i.numpy().decode().split('\t')

        ds = tf_io.read2dataset('title.csv')
        num_part = 3
        batch_size = 4
        for n in range(num_part):
            print(n)
            for i in itertools.islice(ds, batch_size*n, batch_size*(n+1)):
                i.numpy().decode().split('____')
    """
    pattern = _process_pattern(pattern)

    try:
        fs = tf.io.gfile.glob(pattern)
    except Exception as e:
        logger.error(e)
        fs = tf.data.Dataset.list_files(file_pattern=pattern)
        fs = [f.decode() for f in fs.as_numpy_iterator()]

    logger.info("FILES: " + '\t' + '\n\t'.join(fs))

    ds = tf.data.__getattribute__(fmt)(fs, num_parallel_reads=num_parallel_reads)
    return ds


def ds2df(input, sep='\t', columns=None, num_parallel_reads=6):
    ds = read2dataset(input, num_parallel_reads=num_parallel_reads)
    df = pd.DataFrame(
        map(lambda r: r.decode().split(sep), tqdm(ds.as_numpy_iterator())),
        columns=columns
    )
    return df


# 文件复制到本地读写：更快更方便
def read_hdfs(pattern, reader=pd.read_csv, max_workers=1, cache_dir='read_cache', is_union=True):
    """支持多文件读取"""
    files = tqdm(cp(pattern, cache_dir))

    if max_workers == 1:
        dfs = map(reader, files)
    else:
        dfs = files | xProcessPoolExecutor(reader, max_workers) | xlist

    if is_union:
        return pd.concat(dfs, ignore_index=True)
    else:
        return dfs


def to_hdfs(
        df, file_or_dir, batch_size=None,  # 如果拆成很多小文件，file_or_dir应该填入目录
        writer=lambda df, file: df.to_csv(file, sep='\t', header=False, index=False),
        with_success=True,
        cache_dir='to_cache',
        file_start_index=0,
        file_suffix='',
        workers=1,
):
    if_not_exist_makedir(cache_dir)
    file_or_dir = _process_hdfs_path(file_or_dir)

    if batch_size:
        target_dir = file_or_dir

        def _writer(args):
            i, df = args
            writer(df, f"{cache_dir}/part-{i}-{file_suffix}")

        dfs = df_split(df, batch_size=batch_size)
        if workers == 1:
            for args in tqdm(enumerate(dfs, file_start_index)):
                _writer(args)
        else:
            enumerate(dfs, file_start_index) | xProcessPoolExecutor(_writer, workers) | xlist  # 多进程好像会卡死

    else:  # todo弃用这个方案
        name = Path(file_or_dir).name
        target_dir = Path(file_or_dir).parent.__str__().replace('hdfs:/', 'hdfs://')

        writer(df, f"{cache_dir}/{name}")

    cp(cache_dir, target_dir, with_success=with_success)  # 多线程cp
    magic_cmd(f"rm -rf {cache_dir}/*")  # 用完即焚，节省本地内存


if __name__ == '__main__':
    print(check_path("/Users/yuanjie/Desktop/Projects/Python/MeUtils/meutils/data/_SUCCESS"))
    print(check_path_wait("/Users/yuanjie/Desktop/Projects/Python/MeUtils/meutils/data/__SUCCESS"))
