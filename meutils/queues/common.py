#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2023/7/20 10:35
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from queue import Queue


class KeyQueue(object):
    """支持 redis 做队列"""

    def __init__(self, keys: list, queue=None, queue_name='__queue__'):
        self._queue = queue or Queue()
        self.queue_name = queue_name
        for key in keys:  # 初始化队列
            if isinstance(self._queue, Queue):
                self._queue.put(key)
            else:
                self._queue.rpush(queue_name, key)

    def get_and_put(self, n: int = 1):
        for _ in range(n):
            if isinstance(self._queue, Queue):
                element = self._queue.get()
                self._queue.put(element)
            else:
                element = self._queue.blpop(self.queue_name)
                self._queue.rpush(self.queue_name, element)

            yield element

    @property
    def queue(self):
        _ = self._queue.queue if isinstance(self._queue, Queue) else self._queue.lrange(self.queue_name, 0, -1)
        return list(_)


if __name__ == '__main__':
    kq = KeyQueue(list(range(10)), Queue())

    print(kq.queue)
    print(list(kq.get_and_put(1)))
    print(kq.queue)
    print(list(kq.get_and_put(2)))
    print(kq.queue)

    import redis

    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)  # 集群版呢？

    kq = KeyQueue(list(range(10, 20)), queue=r)

    print(kq.queue)
    print(list(kq.get_and_put(1)))
    print(kq.queue)
    print(list(kq.get_and_put(2)))
    print(kq.queue)
