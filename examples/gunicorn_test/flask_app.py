#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : app
# @Time         : 2019-11-21 11:04
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

import os
import time
from flask import Flask

app = Flask(__name__)



# os.system(f"echo {time.ctime()} >> ./log/test.log")


@app.route('/')
def index():
    return 'hello world!'

if __name__ == '__main__':
    app.run('0.0.0.0')
