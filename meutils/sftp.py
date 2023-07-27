#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : sftp
# @Time         : 2022/9/26 上午11:19
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :  sftp -P 57891 comp_5153@222.76.203.180


import paramiko


class SFTPClient(object):

    def __init__(self, host='222.76.203.180', port=57891, username='comp_5153', password='7NmIt00rGF5vKGlt'):
        sf = paramiko.Transport((host, port))
        sf.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(sf)

    def put(self, localpath, remotepath):
        self.sftp.put(localpath, remotepath)


def submit(localpath, remotepath, username, password, sock):
    import paramiko

    with paramiko.Transport(sock) as sf:
        sf.connect(username=username, password=password)

        sftp = paramiko.SFTPClient.from_transport(sf)
        sftp.put(localpath, remotepath)
