#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : monitor
# @Time         : 2022/7/13 下午1:28
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import typer
from meutils.pipe import *
from meutils.tools import service_monitor as _service_monitor


@cli.command()
def service_monitor(filename):
    """传入配置文件"""
    _ = _service_monitor.main(filename)

    typer.echo(_)


@cli.command()
def xx(filename):
    """传入配置文件"""
    return _service_monitor.main(filename)


if __name__ == '__main__':
    cli()
