#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : bar
# @Time         : 2023/3/21 09:20
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from time import sleep
from gooey import Gooey, GooeyParser
from itertools import cycle

@Gooey(
    terminal_font_family='Courier New',
    progress_regex=r"^progress: (?P<current>-?\d+)/(?P<total>\d+)$",
    progress_expr="current / total * 100",
    timing_options={
        'show_time_remaining':True,
        'hide_time_remaining_on_complete':False
    })
def parse_args():
    parser = GooeyParser(prog="example_progress_bar_5")
    parser.add_argument("alpha", type=float, help="Seconds per 10% progress", default=1)
    parser.add_argument("beta", type=int, help="Extra messages between progress updates",default=3)
    parser.add_argument("gamma", type=str, nargs='+', help="List of your messages",
        default=["info ...", "message ...", "warning ..."])
    args = parser.parse_args()
    return args.alpha, args.beta, args.gamma

def main():
    alpha, beta, gamma = parse_args()
    myprocess = cycle(gamma)

    print("Step 1")
    for i in range(0, 51, 10):
        sleep(alpha)
        print("progress: {}/{}".format(i,100),flush=True)

    print("Step 2")
    for i in range(50, 101, 10):
        sleep(alpha / (beta+1))
        for j in range(beta):
            # some extra text before progress
            print(next(myprocess),flush=True)
            sleep(alpha / (beta+1))
        print("progress: {}/{}".format(i,100),flush=True)

if __name__ == "__main__":
    main()