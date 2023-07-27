#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : demo
# @Time         : 2022/4/1 下午6:25
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


def transformers_download(model_name='ckiplab/albert-tiny-chinese', type='torch', out=None):
    if out is None:
        out = Path(model_name)
    else:
        out = Path(out) / Path(model_name)
    out.mkdir(parents=True, exist_ok=True)

    from meutils.request_utils.crawler import Crawler

    files = (
        Crawler(f'https://huggingface.co/{model_name}/tree/main')
            .xpath("/html/body/div[1]/main/div/section/ul/li[*]/a[1]/span[1]//text()")
    )

    files = [file for file in files if file.endswith('.txt') or file.endswith('.json')]

    type2name = {
        'torch': 'pytorch_model.bin',
        'tensorflow': 'tf_model.h5',
        'flax': 'flax_model.msgpack'

    }
    if type == 'all':
        model_files = list([type2name.values()])
    else:
        model_files = [type2name.get(type, 'torch')]

    tqdm_ = tqdm(files + model_files)
    for file in tqdm_:
        tqdm_.set_description(file)
        url = f"https://huggingface.co/{model_name}/resolve/main/{file}"
        wget.download(url, str(out))

def transformers_download(model_name: str, type='torch', out=None):
    """mecli td --model-name ckiplab/albert-tiny-chinese"""

    if out is None:
        out = Path(model_name)
    else:
        out = Path(out) / Path(model_name)

    if out.exists():
        return f'{model_name} already exist'

    out.mkdir(parents=True, exist_ok=True)

    from meutils.request_utils.crawler import Crawler

    files = (
        Crawler(f'https://huggingface.co/{model_name}/tree/main')
            .xpath("/html/body/div[1]/main/div/section/ul/li[*]/a[1]/span[1]//text()")
    )

    files = [file for file in files if file.endswith('.txt') or file.endswith('.json')]

    type2name = {
        'torch': 'pytorch_model.bin',
        'tensorflow': 'tf_model.h5',
        'flax': 'flax_model.msgpack'

    }
    if type == 'all':
        model_files = list([type2name.values()])
    else:
        model_files = [type2name.get(type, 'torch')]

    tqdm_ = tqdm(files + model_files)
    for file in tqdm_:
        tqdm_.set_description(file)
        url = f"https://huggingface.co/{model_name}/resolve/main/{file}"
        wget.download(url, str(out))

if __name__ == '__main__':
    transformers_download("ckiplab/albert-tiny-chinese")
