#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : b
# @Time         : 2021/1/31 9:02 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 


import typer


cli = typer.Typer(name="CLI DEMO")


@cli.command('a')
def hello(name: str):
    typer.echo(f"Hello {name}")

if __name__ == "__main__":
    cli()