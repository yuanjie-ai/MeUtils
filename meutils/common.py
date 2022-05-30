#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : common
# @Time         : 2020/11/12 11:42 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 单向引用，避免循环引用


import os
import gc
import re
import sys
import time
from abc import abstractmethod

import wget
import zipfile
import joblib
import datetime
import operator
import inspect
import requests
import socket
import warnings
import argparse
import yaml
import fire
import itertools
import subprocess
import wrapt
import traceback
import multiprocessing
import base64
import typer
import shutil
import asyncio
import importlib
import random

import numpy as np
import pandas as pd

from typing import *
from PIL import Image, ImageGrab

from pathlib import Path
from loguru import logger
from tqdm.auto import tqdm
from contextlib import contextmanager
from functools import reduce, lru_cache
from collections import Counter, OrderedDict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pydantic import BaseModel, Field

# 第三方
from faker import Faker  # https://www.cnblogs.com/aichixigua12/p/13236092.html

# ME
from meutils.hash_utils import murmurhash

from meutils.crontab import CronTab
from meutils.besttable import Besttable
from meutils.decorators import args, singleton
from meutils.path_utils import get_module_path, get_resolve_path
from meutils.cache_utils import ttl_cache, disk_cache

try:
    import simplejson as json
except ImportError:
    import json

try:
    import dill as pickle
except ImportError:
    import pickle

warnings.filterwarnings("ignore")
tqdm.pandas(ncols=66)

cli = typer.Typer(name="CLI")

# 常量
START_TIME = time.time()
CPU_NUM = os.cpu_count()
HOST_NAME = socket.getfqdn(socket.gethostname())
try:
    LOCAL_HOST = socket.gethostbyname(HOST_NAME)
except:
    LOCAL_HOST = '127.0.0.1'

LOCAL = LOCAL_HOST == "127.0.0.1"

# json: dict -> str
dict2json = bjson = lambda dic: json.dumps(dic, indent=4, ensure_ascii=False)
json2dict = lambda s: json.loads(s.replace("'", '"'))


# image
# im = ImageGrab.grabclipboard() 获取剪切板的图片


class BaseConfig(BaseModel):
    """基础配置"""
    _path: str = None

    @classmethod
    def init(cls):
        """init from path[zk/yaml]"""
        assert cls._path is not None, "请指定 _path"
        return cls.parse_path(cls._path)

    @classmethod
    def parse_path(cls, path):
        if Path(path).is_file():
            return cls.parse_yaml(cls._path)
        else:
            return cls.parse_zk(cls._path)

    @classmethod
    def parse_yaml(cls, path):
        with open(path) as f:
            json = yaml.load(f)
            return cls.parse_obj(json)

    @classmethod
    def parse_zk(cls, path):
        from meutils.zk_utils import get_zk_config
        json = get_zk_config(path)
        return cls.parse_obj(json)

    @classmethod
    def parse_env(cls):
        return cls.parse_obj(os.environ)


class Main(object):
    """
    if __name__ == '__main__':
        "一大堆业务逻辑"
        class TEST(Main):

            @args
            def main(self, **kwargs):
                print(kwargs)


        TEST.cli()
    """

    @args
    def main(self, **kwargs):
        """重写入口函数
        可用BaseConfig控制参数类型
        """
        pass

    @classmethod
    def cli(cls):
        """命令行"""
        logger.debug(f'MAIN: {cls.__name__}')
        fire.Fire(cls)  # 不支持__init__参数


@contextmanager
def timer(task="Task"):
    """https://www.kaggle.com/lopuhin/mercari-golf-0-3875-cv-in-75-loc-1900-s
        # 其他装饰器可学习这种写法
        with timer() as t:
            time.sleep(3)

        @timer()
        def f():
            print('sleeping')
            time.sleep(6)
            return 6
    """

    logger.info(f"{task} started")
    s = time.time()
    yield
    e = time.time()
    logger.info(f"{task} done in {e - s:.3f} s")


# limit memory
def limit_memory(memory=16):
    """
    :param memory: 默认限制内存为 16G
    :return:
    """
    import resource

    rsrc = resource.RLIMIT_AS
    # res_mem=os.environ["RESOURCE_MEM"]
    memlimit = memory * 1024 ** 3
    resource.setrlimit(rsrc, (memlimit, memlimit))
    # soft, hard = resource.getrlimit(rsrc)
    logger.info("memory limit as: %s G" % memory)


def magic_cmd(cmd='ls', parse_fn=lambda s: s, print_output=False):
    """

    :param cmd:
    :param parse_fn: lambda s: s.split('\n')
    :param print_output:
    :return:
    """
    cmd = ' '.join(cmd.split())
    status, output = subprocess.getstatusoutput(cmd)
    output = output.strip()

    logger.info(f"CMD: {cmd}")
    logger.info(f"CMD Status: {status}")

    if print_output:
        logger.info(f"CMD Output: {output}")

    return status, parse_fn(output)


def download(url, rename=None):
    """
    wget.download(url, out=target_name)
    """
    cmd = f"wget {url}"
    if rename:
        cmd += f" -O {rename}"

    os.system(cmd)


def yaml_load(path):
    path = get_module_path(path)
    with open(path) as f:
        return yaml.load(f)


def dict2yaml(dic, file=None):
    s = yaml.dump(dic)
    print(s)

    if file:
        with open(file, 'w') as f:
            f.write(s)


def git_pull(repo='dsl3'):
    repo_name = repo.split('/')[-1][:-4]
    if Path(repo_name).exists():
        magic_cmd(f'cd {repo_name} && git pull')
    else:
        magic_cmd(f'git clone {repo}')


list4log = lambda ls: "\n\t" + "\n\t".join(ls)


def clear(ignore=('TYPE_CHECKING', 'logger', 'START_TIME', 'CPU_NUM', 'HOST_NAME', 'LOCAL_HOST', 'LOCAL')):
    """销毁全局变量
    TODO：可添加过滤规则
    """
    keys = []
    ignore = set(ignore)
    for key, value in globals().items():
        if key.startswith('_') or key in ignore:
            continue
        if callable(value) or value.__class__.__name__ == "module":
            continue
        keys.append(key)

    logger.debug("销毁全局变量: " + list4log(keys))
    for key in keys:
        del globals()[key]
    return keys


def dic2obj(dic):
    class Kwargs:
        pass

    kwargs = Kwargs()
    kwargs.__dict__ = dic
    return kwargs


def dict_flatten(dic: dict):
    """
        d = {'a': range(10), 'b': range(20)}
        [(k, i) for k, v in d.items() for i in v]

    :param dic:
    :return:
    """
    return [(k, i) for k, v in dic.items() for i in v]


def bytes2base64(bytes_data):
    return base64.b64encode(bytes_data).decode()


# try:
#     from pysnooper import snoop as debug
# except ImportError:
#     os.system('pip install -U --no-cache-dir pysnooper')
#
# finally:
#     if os.environ.get('debug') == '0':  # os.environ['debug'] = '0'
#         from meutils.decorators.decorator import decorator
#
#
#         @decorator
#         def debug(func, *args, **kwargs):
#             return func(*args, **kwargs)


def is_open(ip='88.01.012.01'[::-1], port=7000, timeout=1):
    """
        os.system(f"ping {'88.01.012.01'[::-1]} -c 1 -W 1 > IS_PRODUCT") == 0

    @param ip:
    @param port:
    @param timeout:
    @return:
    """
    if ':' in ip:
        ip, port = ip.split(':')

    socket.setdefaulttimeout(timeout)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((ip, int(port)))
            s.shutdown(socket.SHUT_RDWR)
            return True
        except:
            return False


class Encrypt(object):
    """加密"""

    def __init__(self, key=2):
        self.key = key

    def encrypt(self, s):
        b = bytearray(str(s).encode("utf-8"))
        n = len(b)
        c = bytearray(n * 2)
        j = 0
        for i in range(0, n):
            b1 = b[i]
            b2 = b1 ^ self.key
            c1 = b2 % 19
            c2 = b2 // 19
            c1 = c1 + 46
            c2 = c2 + 46
            c[j] = c1
            c[j + 1] = c2
            j = j + 2
        return c.decode("utf-8")

    def decrypt(self, s):
        c = bytearray(str(s).encode("utf-8"))
        n = len(c)
        if n % 2 != 0:
            return ""
        n = n // 2
        b = bytearray(n)
        j = 0
        for i in range(0, n):
            c1 = c[j]
            c2 = c[j + 1]
            j = j + 2
            c1 = c1 - 46
            c2 = c2 - 46
            b2 = c2 * 19 + c1
            b1 = b2 ^ self.key
            b[i] = b1
        return b.decode("utf-8")


def sys_path_append(path, __file__=None):
    """添加home到系统

    @param path:
    @return: home绝对路径
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


def list_difference(l1, l2):
    """列表差集，保持l1的顺序"""
    s = frozenset(l2)
    return [i for i in l1 if i not in s]


def list_intersection(l1, l2):
    """列表交集，保持l1的顺序"""

    s = frozenset(l2)
    return [i for i in l1 if i in s]


if __name__ == '__main__':
    with timer() as t:
        time.sleep(3)

    status, output = magic_cmd('ls')
    print(status, output)

    d = {'a': 1, 'b': 2}
    print(bjson(d))
    print(BaseConfig.parse_obj(d))
