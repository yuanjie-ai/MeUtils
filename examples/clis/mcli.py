#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : mcli
# @Time         : 2022/1/17 下午1:51
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *


class TEST(Main):

    @args
    def main(self, **kwargs):
        print(kwargs)
        pass


TEST.cli()
