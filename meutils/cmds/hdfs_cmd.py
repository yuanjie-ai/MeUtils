#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : hdfs_cmd
# @Time         : 2021/1/20 10:15 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


class HDFS(object):
    HADOOP_HOME = os.environ.get('HADOOP_HOME', '~/infra-client/bin')
    HDFS_CLUSTER_NAME = os.environ.get('HDFS_CLUSTER_NAME', 'zjyprc-hadoop')

    HDFS_CMD = f"{HADOOP_HOME}/hdfs --cluster {HDFS_CLUSTER_NAME} dfs"  # f"{HADOOP_HOME}/hadoop --cluster {HDFS_CLUSTER_NAME} fs"

    @classmethod
    def check_path_isexist(cls, path):
        cmd = f"-test -e {path}"  # 包含？-test -d
        status, output = cls.magic_cmd(cmd)

        rst = False if status != 0 else True
        logger.info(f'Path Exist: {rst}')

        return rst

    @classmethod
    def touchz(cls, path):
        """

        :param path: /user/h_browser/algo/yuanjie/jars/xx.txt
        :return:
        """
        cmd = f"-touchz {path}"
        return cls.magic_cmd(cmd)

    @classmethod
    def wc_l(cls, path):
        """

        :param path: /user/h_data_platform/platform/browser/push_group/locals/江苏_南京/date=20210120/*
        :return:
        """
        cmd = f"-cat {path} | wc -l"
        return cls.magic_cmd(cmd)

    @classmethod
    def magic_cmd(cls, cmd):
        """

        :param cmd: -cat /user/h_browser/algo/yuanjie/jars/vec.csv
        :return:
        """
        cmd = f"{cls.HDFS_CMD} {cmd}"
        return magic_cmd(cmd)

    @classmethod
    def push2hdfs(cls, input, output):
        cls.magic_cmd(f"-mkdir -p {output}")
        cls.magic_cmd(f"-put -f {input} {output}")
        cls.touchz(f"{output}/_SUCCESS")
