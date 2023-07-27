#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : __init__.py
# @Time         : 2021/1/31 10:20 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : python meutils/clis/__init__.py


import typer

from meutils.pipe import *
from meutils.notice.wecom import Wecom

cli = typer.Typer(name="MeUtils CLI")
logger = logger.patch(lambda r: r.update(name=__file__))


@cli.command(help="help")  # help会覆盖docstring
def clitest(name: str):
    """

    @param name: name
    @return:
    """
    typer.echo(f"Hello {name}")



@cli.command()
def zk2file(zk_path, mode='yaml', filename=None):
    """本地可再同步到hdfs

     mecli zk2file /push/zk2yaml/train.yaml --mode yaml --filename new.yaml

    :param zk_path:
    :param mode:
    :param filename: 不为空可覆盖
    :return:
    """
    from meutils.zk_utils import get_zk_config
    zk_conf = get_zk_config(zk_path, mode=mode)

    if filename is None:
        filename = zk_path.split('/')[-1]

    with open(filename, 'w') as f:
        if mode == 'yaml':
            yaml.dump(zk_conf, f)
        else:
            f.write(zk_conf)


@cli.command()
def push_docker(ContainerID, ImageName='app:latest', author='yuanjie', message='update'):
    """自定义镜像"""
    url = 'eijnauy/ten.imoaix.d.rc'[::-1]
    cmd = f"docker commit  -a {author} -m {message} {ContainerID} {url}/{ImageName} && docker push {url}/{ImageName}"
    magic_cmd(cmd)


@cli.command()
def loop_cmd(cmd, args: str, sep=','):
    """mecli loop-cmd 'ls {arg}' ".,.."""

    for arg in tqdm(args.split(sep)):
        magic_cmd(cmd.format(arg=arg), print_output=True)


@cli.command()
def register_ip(path, sleep_time: int = -1):
    """mecli register-ip /push/ann/ips --sleep-time 10"""
    from meutils.zk_utils import register_ip as _register_ip
    _register_ip(path, sleep_time)


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


@cli.command(help=None)
def pkg(template='pypackage'):
    """python package template"""

    try:
        from cookiecutter.main import cookiecutter

        template_path = get_module_path(f"../templates/{template}", __file__)

        pkg_path = cookiecutter(template_path)

        for p in Path(pkg_path).rglob('__pycache__'):
            if p.exists():  # shutil.rmtree(p, True)
                shutil.rmtree(p)  # p.rmdir() 只能删除为空的

    except ImportError as info:
        logger.error(info)



if __name__ == '__main__':
    cli()
