#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : cmd
# @Time         : 2021/2/24 2:28 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import magic_cmd

# build
cmd = 'docker build -f Dockerfile:milvus .'
magic_cmd(cmd)

# push
r = magic_cmd('docker container ls')[1][1]
print(r)
container_id = r.split()[0]

author = 'yuanjie'
ContainerID = container_id
message = 'msg'
ImageName = 'milvus:1.0'

url = 'eijnauy/ten.imoaix.d.rc'[::-1]
cmd = f"docker commit  -a {author} -m {message} {ContainerID} {url}/{ImageName} && docker push {url}/{ImageName}"
print(magic_cmd(cmd, print_output=True)[0])
