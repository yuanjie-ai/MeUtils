#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : gunicorn
# @Time         : 2019-11-21 11:00
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : supervisor https://www.cnblogs.com/wxwgk/p/13258401.html
# https://www.jianshu.com/p/fecf15ad0c9a
# https://blog.csdn.net/qq_43475458/article/details/108059922
# https://www.cnblogs.com/john-xiong/p/13991400.html
# https://www.jianshu.com/p/260f18aa5462
# https://docs.gunicorn.org/en/latest/settings.html#threads


from meutils.pipe import *
from gunicorn.glogging import Logger

Logger.access_fmt = Logger.error_fmt
# 启动的进程数
# daemon 开启后台
# reload = True
preload = True

port = 8501
bind = f'0.0.0.0:{port}'
workers = 1  # 2 * CPU_NUM + 1
threads = 1
worker_class = 'uvicorn.workers.UvicornWorker'

# 日志
chdir = "/Users/yuanjie/Desktop/Projects/Python/MeUtils/examples/gunicorn_test/app"
logdir = Path(chdir) / 'log'
logdir.mkdir(exist_ok=True)

loglevel = 'error'
pidfile = f'{logdir}/pidfile'
errorlog = '-'  # f'{logdir}/app_error.log'
accesslog = f'{logdir}/app_access.log'  # '-'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'  # 设置gunicorn访问日志格式，错误日志无法设置

# settings
timeout = 30
graceful_timeout = 60
keepalive = 3

if __name__ == '__main__':
    os.system(f"gunicorn -c {__file__} main:app --chdir /Users/yuanjie/Desktop/Projects/Python/MeUtils/examples/gunicorn_test/app/xx")
