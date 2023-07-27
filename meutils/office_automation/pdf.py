#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : pdf
# @Time         : 2022/6/30 下午3:41
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


def extract_text(file_or_text):
    import fitz  # pymupdf 速度更快

    _bytes = b''
    if isinstance(file_or_text, (str, Path)) and Path(file_or_text).is_file():
        _bytes = Path(file_or_text).read_bytes()
    elif isinstance(file_or_text, bytes):
        _bytes = file_or_text

    else:
        return file_or_text

    return '\n'.join(page.get_text().strip() for page in fitz.Document(stream=_bytes))


def pdf2text(file_or_dir_or_files, n_jobs=3):
    if isinstance(file_or_dir_or_files, str) or not isinstance(file_or_dir_or_files, Iterable):
        p = Path(file_or_dir_or_files)
        if p.is_file():
            file_or_dir_or_files = [p]
        elif p.is_dir():
            file_or_dir_or_files = p.glob('*.pdf')
        else:
            raise ValueError('无效文件')

    _ = file_or_dir_or_files | xJobs(lambda p: (p, extract_text(p)), n_jobs)

    return pd.DataFrame(_, columns=['filename', 'text'])


def pdf2table(filename, pages='1', suppress_stdout=False, **kwargs):
    import camelot
    tables = camelot.read_pdf(filename, pages=pages, suppress_stdout=suppress_stdout, **kwargs)
    for t in tables:
        yield t.df


def doc2text(filename):
    pass


def doc2text(filename):
    pass


if __name__ == '__main__':
    pass
