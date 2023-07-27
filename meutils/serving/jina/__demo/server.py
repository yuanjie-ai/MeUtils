#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : server
# @Time         : 2022/9/9 下午4:59
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from jina import Document, DocumentArray, Executor, Flow, requests, Deployment


class E(Executor):
    @requests  # 默认串起来
    def func(self, docs: DocumentArray, **kwargs):
        for d in docs:
            d.text += 'None'


class EE(Executor):
    @requests
    def func(self, docs: DocumentArray, **kwargs):
        for d in docs:
            d.text += 'Null'


class E1(Executor):
    @requests(on='/e1')
    def func(self, docs: DocumentArray, **kwargs):
        for d in docs:
            d.text += '1'


class E2(Executor):
    @requests(on='/e2')
    def func(self, docs: DocumentArray, **kwargs):
        for d in docs:
            d.text += '2'


f1 = Flow(port=8501).add(uses=E)
f2 = Flow(port=8502).add(uses=E1)
f12 = Flow(port=8503).add(uses=E).add(uses=E1)
f123 = (
    Flow(port=8504)
    .add(uses=E, name='E').add(uses=EE, name='EE')
    .add(uses=E1, needs='E')
    .add(uses=E2, needs='EE')
)
# f123 = (
#     Flow(port=8506)
#     .add(uses=E, name='E').add(uses=EE, name='EE')
#     .add(uses=E1, name='E1')
#     .add(uses=E2, needs=['E1'])
# )

# f = Flow(port=8501, protocol=['GRPC']).add(uses=MyExec).add(uses=Cut)
# f = Flow(port=[8500, 8501], protocol=['GRPC', 'HTTP']).add(uses=MyExec)  # .add(uses=Cut).add(uses=Read)
f123.plot('flow.svg')



if __name__ == '__main__':

    with f1, f2, f12, f123:
        # 测试
        r = f1.post('/', DocumentArray.empty(1))
        print(r.texts)
        r = f2.post('/e1', DocumentArray.empty(2))
        print(r.texts)
        # r = f12.post('/e2', DocumentArray.empty(12))
        # print(r.texts)
        # r = f123.post('/', DocumentArray.empty(3))
        # print(r.texts)
        # r = f123.post('/', [1,2,3])
        # backend server forever
        # f123.block()

    # with Deployment(name='myexec1', uses=MyExec) as dep:
    #     dep.post(on='/bar', inputs=Document(), on_done=print)


