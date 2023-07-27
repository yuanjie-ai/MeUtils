#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2023/5/18 16:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


def doc2docx(doc_paths, outdir='.', max_workers=1):
    """todo: 多进程阻塞"""
    if isinstance(doc_paths, str):
        doc_paths = [doc_paths]
    max_workers = min(max_workers, len(doc_paths))
    func = partial(_doc2docx, outdir=outdir)
    return doc_paths | xProcessPoolExecutor(func, max_workers) | xlist


def _doc2docx(doc_path, outdir='.'):
    if Path(doc_path).is_file():
        cmd = 'libreoffice --headless --convert-to docx'.split() + [doc_path, '--outdir', outdir]
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        p.wait(timeout=16)
        stdout, stderr = p.communicate()
        if stderr:
            raise subprocess.SubprocessError(stderr)
        return stdout.decode()
    return False
