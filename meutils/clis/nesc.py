#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : wecom
# @Time         : 2021/9/6 下午5:21
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


import typer

from meutils.pipe import *
from meutils.notice import nesc_send as nesc_send_
from meutils.notice.wecom import Wecom

cli = typer.Typer(name="MeUtils CLI")


@cli.command()
def notice(title, text='', hook_url=None):
    """sh管道传参 echo args | xargs -I {} mecli notice {}"""
    Wecom(hook_url).send_markdown(title, text)
    return 'ok'


@cli.command()
def wecom_send_file(path, type='file', hook_url=None):
    """mecli notice file_path"""
    Wecom(hook_url).send_file(path, type)
    return 'ok'


@cli.command()
def notice(content, chat_id=1162363786, appid='ai', filename=None):
    """echo args | xargs -I {} nesc notice {}"""
    return nesc_send_(content=content, chat_id=chat_id, appid=appid, filename=filename)


if __name__ == '__main__':
    cli()
