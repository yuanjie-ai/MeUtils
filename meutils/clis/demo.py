#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : demo
# @Time         : 2022/11/11 下午12:17
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


import typer
from meutils.pipe import *
from meutils.tools import service_monitor as _service_monitor

cli = typer.Typer(name="MeUtils CLI")


@cli.command()
def args(
        a: str = typer.Option(...),
        b: int = typer.Option(...),
        c: bool = typer.Option(False, help='is helper'),

):
    print(a, b, c)


if __name__ == '__main__':
    cli()
