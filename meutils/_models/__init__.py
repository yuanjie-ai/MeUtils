#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : __init__.py
# @Time         : 2020/12/2 10:43 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  :

import os
import yaml
import json
from pathlib import Path
from pydantic import BaseModel, Field


def _print_cfg(obj):
    print(json.dumps(obj, indent=4, ensure_ascii=False))


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
        """

        :param path: zk/yaml
        :return:
        """

        if Path(path).is_file():
            return cls.parse_yaml(cls._path)
        else:
            return cls.parse_zk(cls._path)

    @classmethod
    def parse_yaml(cls, path):
        with open(path) as f:
            json = yaml.load(f)
            _print_cfg(json)

            return cls.parse_obj(json)

    @classmethod
    def parse_zk(cls, path):
        from meutils.zk_utils import get_zk_config
        json = get_zk_config(path)

        _print_cfg(json)

        return cls.parse_obj(json)

    @classmethod
    def parse_env(cls, path=None):
        """

        :param path: 默认读取所有环境变量
        :return:
        """
        env = os.environ.get(path, {}) if path else os.environ
        return cls.parse_obj(env)
