#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : dict2yaml
# @Time         : 2021/2/5 3:39 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


def get_config(config_init=None):
    if isinstance(config_init, dict):
        pass
    elif isinstance(config_init, str) and Path(config_init).is_file():
        p = Path(config_init)

        if p.name.endswith('.json'):
            config_init = json.loads(p.read_bytes())

        elif p.name.endswith('.yaml') or p.name.endswith('.yml'):
            config_init = yaml.safe_load(p.read_bytes())

        else:
            raise ValueError("目前只支持 json/yaml")

    else:
        config_init = {}

    return config_init


if __name__ == '__main__':
    print(get_config({"a": 1}))
    print(get_config('dict2yaml.yaml'))
