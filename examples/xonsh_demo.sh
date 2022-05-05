#!/usr/bin/env /Users/yuanjie/Library/Python/3.7/bin/xonsh
# @Project      : MeUtils
# @Time         : 2021/12/23 下午5:36
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

from meutils.pipe import *
from rich.progress import track

for i in tqdm(range(100)):
    echo @(i)
    time.sleep(0.01)

#for i in track(range(100)):
#    time.sleep(0.01)