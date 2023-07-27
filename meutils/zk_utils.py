#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : zk_utils
# @Time         : 2020/11/11 5:49 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

import time
import yaml
import socket
from pathlib import Path
from loguru import logger
from kazoo.client import KazooClient

try:
    zk = KazooClient(hosts='', timeout=1)
    zk.start()
    zk_get_children = zk.get_children  # 获取所有节点

except Exception as e:
    logger.exception(e)
    pass


class ZKConfig(object):
    """便于实时监控zk配置"""
    info = None


def zk_watcher(path, zk_hosts=''):
    """实时监控"""

    zk = KazooClient(hosts=zk_hosts)
    zk.start()

    @zk.DataWatch(path)
    def watcher(data, stat):
        logger.info(f'zk stat: {stat}')
        ZKConfig.info = yaml.safe_load(data)

    return watcher


def zk_logger(log, path='/push/log'):
    if not zk.exists(path):
        zk.create(path, log.encode(), makepath=True)
    else:
        zk.set(path, log.encode())


# @zk.DataWatch('/push/nh_model')
# def watcher(data, stat):  # (data, stat, event)
#     ZKConfig.info = yaml.safe_load(data)

def get_zk_config(zk_path="/push/cfg", hosts='', mode='yaml'):
    zk = KazooClient(hosts)
    zk.start()

    data, stat = zk.get(zk_path)

    if mode == 'yaml':
        return yaml.safe_load(data)
    else:
        return data.decode()


def register_ip(path='/push/ann/ips', sleep_time=10):  # 最后需要 /
    """session 中断后自动删除该节点, 实例重启后自动更新节点

    :param path:
    :return:
    """
    import datetime
    s = datetime.datetime.today()

    ip = socket.gethostbyname(socket.gethostname())
    node = str(Path(path) / ip)

    time.sleep(15)

    if not zk.exists(node):
        zk.create(node, str(s).encode(), makepath=True, ephemeral=True)
    else:
        logger.warning(f"{node} alreadly exists")

    if sleep_time == -1:  # 一直监控
        while 1:
            time.sleep(10000)
    else:
        time.sleep(sleep_time)


# 常用固定
class Config(object):
    pass


zk_cfg = Config()
zk_cfg.__dict__ = yaml.safe_load(zk.get('/push/cfg')[0])  # todo: 具体定义下结构更清晰

if __name__ == '__main__':
    # print(get_zk_config("/push/cfg"))
    # zk_logger('log__', '/push/xxx')
    # print(zk_cfg)
    # print(get_zk_config("/push/email_token"))
    register_ip()
