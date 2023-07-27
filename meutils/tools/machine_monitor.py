#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : machine_monitor
# @Time         : 2022/7/14 上午9:03
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://blog.csdn.net/Deaohst/article/details/119132135


import numpy as np
import psutil
from functools import wraps


def source_info():
    cpu_per = psutil.cpu_percent(True, True)
    cpu_per = round(np.array(cpu_per).mean(), 2)
    mem = psutil.virtual_memory()
    cpu_num = psutil.cpu_count(logical=True)
    mem_total = round(mem.total / 2 ** 32, 2)
    mem_per = round(mem.percent, 2)
    disk = []
    partitions = psutil.disk_partitions()
    for i in partitions:
        info = psutil.disk_usage(i[1])
        disk.append([info.total, info.used])
    disk = np.array(disk)
    disk = disk.sum(axis=0)
    disk_pre = round(disk[1] / disk[0] * 100, 2)
    disk_total = round(disk[0] / 2 ** 30, 2)

    return {
        "cpu数量": f"{cpu_num} | {cpu_per}%",
        "内存总量": f"{mem_total}GB | {mem_per}%",
        "磁盘总量": f"{disk_total}GB | {disk_pre}%"
    }


def dev_source_monitor(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        cpu_per = psutil.cpu_percent(True, True)
        cpu_per = round(np.array(cpu_per).mean(), 2)
        mem = psutil.virtual_memory()
        cpu_num = psutil.cpu_count(logical=True)
        mem_total = round(mem.total / 2 ** 32, 2)
        mem_per = round(mem.percent, 2)
        disk = []
        partitions = psutil.disk_partitions()
        for i in partitions:
            info = psutil.disk_usage(i[1])
            disk.append([info.total, info.used])
        disk = np.array(disk)
        disk = disk.sum(axis=0)
        disk_pre = round(disk[1] / disk[0] * 100, 2)
        disk_total = round(disk[0] / 2 ** 30, 2)
        print('设备资源总量')
        print(f"cpu数量:{cpu_num}")
        print(f"内存总量:{mem_total}GB")
        print(f"磁盘总量:{disk_total}GB")
        print("设备资源使用")
        print(f"cpu使用:{cpu_per}%")
        print(f"内存使用:{mem_per}%")
        print(f"磁盘使用:{disk_pre}%")
        # print(decorated.__name__)
        return f(*args, **kwargs)

    return decorated


if __name__ == '__main__':
    # @dev_source_monitor
    # def func():
    #     pass
    #
    #
    # func()

    print(source_info())
