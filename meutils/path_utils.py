#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : path_utils
# @Time         : 2020/11/12 11:39 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

import os
import sys
import json
import zipfile

import yaml

from pathlib import Path
from zipfile import ZipFile
from loguru import logger

get_resolve_path = lambda path, file: (Path(file).parent / Path(path)).resolve()
get_module_path = lambda path, file: os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(file), path))


def file2json(path):
    """yaml/json"""
    p = Path(path)

    o = {}
    if p.is_file():

        if p.name.endswith('.json'):
            o = json.loads(p.read_bytes())

        elif p.name.endswith(('.yml', '.yaml')):
            o = yaml.safe_load(p.read_bytes())
    else:
        logger.error(f"无效地址：{path}")
    return o


def sys_path_append(path, __file__=None):
    """添加home到系统
    """
    if __file__:
        path = get_module_path(path, __file__)

    p = Path(path).resolve()
    if p.is_file():
        py_home = p.parent.__str__()
    elif p.is_dir():
        py_home = p.__str__()
    else:
        raise Exception(f"{path} 为错误路径")

    logger.info(f"{path} HOME: {py_home}")

    sys.path.append(py_home)

    return py_home


def path2list(path, pattern='*'):
    ps = []
    p = Path(path)
    if p.is_file():
        ps = [p]
    elif p.is_dir():
        ps = list(p.glob(pattern))
    else:
        logger.error('ErrorPath !!!')
    return ps


def get_config(config_init=None):
    if isinstance(config_init, str) and Path(config_init).is_file():
        p = Path(config_init)

        if p.name.endswith('.json'):
            config_init = json.loads(p.read_bytes())

        elif p.name.endswith('.yaml') or p.name.endswith('.yml'):
            config_init = yaml.safe_load(p.read_bytes())

        else:
            logger.error('目前只支持dict/json/yaml格式')
            config_init = {}

    else:
        config_init = config_init if config_init else {}

    return config_init


def get_import_module_path(name='paddleocr'):
    import importlib
    return str(importlib.import_module(name)).split()[-1][1:-2]


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
    print(os.getcwd())
    print(os.path.dirname(__file__))
