#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : app
# @Time         : 2021/12/21 下午12:06
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

import typer

from meutils.pipe import *

cli = typer.Typer(name="APP CLI")




@cli.command()
def run(port, workers=1, threads=1, preload=True, loglevel='debug', chdir='.', main_class='main'):
    logdir = Path(chdir) / 'log'
    logdir.mkdir(exist_ok=True)
    errorlog = '-'  # f'{logdir}/app_error.log'
    accesslog = f'{logdir}/app_access.log'  # '-'
    pidfile = f'{logdir}/pidfile'

    cmd = f"""
    gunicorn --bind 0.0.0.0:{port}
    --workers {workers}
    --threads {threads}
    --worker-class uvicorn.workers.UvicornWorker
    --timeout 30
    --graceful-timeout 60
    --keep-alive 3
    --log-level {loglevel}
    --error-logfile {errorlog}
    --access-logfile {accesslog}
    --pid {pidfile}
    --preload_app {preload}
    {main_class}:app
    """.strip().replace('\n', ' ')

    os.system(cmd)
