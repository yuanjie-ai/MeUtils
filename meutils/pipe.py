#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : pipe_utils
# @Time         : 2020/11/12 11:35 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

import functools
from meutils.common import *


class Pipe(object):
    """I am very like a linux pipe"""

    def __init__(self, function):
        self.function = function
        functools.update_wrapper(self, function)

    def __ror__(self, other):
        return self.function(other)

    def __call__(self, *args, **kwargs):
        return Pipe(lambda x: self.function(x, *args, **kwargs))


########### 常用管道函数
# 进度条
xtqdm = Pipe(lambda iterable, desc=None: tqdm(iterable, desc, ncols=66))

# base types
xtuple, xlist, xset = Pipe(tuple), Pipe(list), Pipe(set)
xarray = Pipe(lambda x, decimals=None: np.array(x) if decimals is None else np.round(np.array(x), decimals))

# 高阶函数
xmap = Pipe(lambda iterable, func: map(func, iterable))
xreduce = Pipe(lambda iterable, func: reduce(func, iterable))
xfilter = Pipe(lambda iterable, func=None: filter(func, iterable))

# itertools: https://blog.csdn.net/weixin_43193719/article/details/87536371
xchain = Pipe(lambda iterable: itertools.chain(*iterable))
xbatch = Pipe(lambda iterable, i=0, batch_size=1: itertools.islice(iterable, i * batch_size, (i + 1) * batch_size))

xunique = Pipe(lambda iterable: list(OrderedDict.fromkeys(list(iterable))))  # 移除列表中的重复元素(保持有序)

"""多个df: 
dfs = (
    Path('.').glob('demo*.txt') | xmap(lambda p: pd.read_csv(p, chunksize=2, names=['id'])) | xchain
)
"""
# str
xjoin = Pipe(lambda chars, sep=' ': sep.join(map(str, chars)))
xsort = Pipe(lambda iterable, reverse=False: sorted(iterable, reverse=reverse))
xgetitem = Pipe(lambda iterable, index=0: operator.getitem(iterable, index))
xitemgetter = Pipe(lambda keys: operator.itemgetter(*keys))

xprint = Pipe(lambda s, sep='\n': print(s, sep=sep))

# np

# group
xgroup = Pipe(lambda ls, step=3: [ls[idx: idx + step] for idx in range(0, len(ls), step)])

# 调试用
xnext = Pipe(lambda ls: iter(ls).__next__())



@Pipe
def xshuffle(ls, seed=None):
    ls = ls.copy()
    random.shuffle(ls, random=seed)
    return ls


@Pipe
def xHashBins(ls, bins=3):
    """hash分组"""
    dic = {}
    for v in ls:
        dic.setdefault(murmurhash(v, bins=bins), []).append(v)
    return list(dic.values())


# multiple
@Pipe
def xJobs(iterable, func, n_jobs=3):
    """支持匿名函数"""
    delayed_function = joblib.delayed(func)
    return joblib.Parallel(n_jobs=n_jobs)(delayed_function(arg) for arg in iterable)
    # yield from joblib.Parallel(n_jobs=n_jobs)(delayed_function(arg) for arg in iterable)


@Pipe
def xThreadPoolExecutor(iterable, func, max_workers=5):
    """
    with ThreadPoolExecutor(max_workers) as pool:
        pool.map(func, iterable)
    """
    with ThreadPoolExecutor(max_workers) as pool:
        return pool.map(func, iterable)


@Pipe
def xProcessPoolExecutor(iterable, func, max_workers=5):
    """
    with ProcessPoolExecutor(max_workers) as pool:
        pool.map(func, iterable)
    """
    with ProcessPoolExecutor(max_workers) as pool:
        return pool.map(func, iterable)


# operator: 排序、取多个值     https://blog.csdn.net/u010339879/article/details/98304292
# operator.itemgetter(*keys)(dic)

@Pipe
def xDictValues(keys, dic: dict, default=None):
    return tuple(dic.get(k, default) for k in keys)


@Pipe
def xDictRemove(keys, dic: dict):
    for k in keys:
        if k in dic:
            del dic[k]


# 异步
@Pipe
def xAsyncio(tasks, return_exceptions=False):
    """为了从异步方式获益，一个应用程序需要有经常被 I/O 阻塞的任务，并且没有太多 CPU 工作。Web 应用程序通常非常适合，特别是当它们需要处理大量客户端请求时。
        import nest_asyncio
        nest_asyncio.apply()

        from asgiref.sync import sync_to_async

        @sync_to_async(thread_sensitive=False)
        def hello():
            time.sleep(1)
            return time.ctime()

        [hello() for _ in range(10)] | xAsyncio

    """
    loop = asyncio.get_event_loop()
    _ = asyncio.gather(*tasks, return_exceptions=return_exceptions)  # asyncio.wait(tasks)
    return loop.run_until_complete(_)


if __name__ == '__main__':
    @Pipe
    def xfunc1(x):
        _ = x.split()
        print(_)
        return _


    @Pipe
    def xfunc2(x):
        _ = '>>'.join(x)
        print(_)
        return _


    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger.patch(lambda r: r.update(name='__file__', function=func.__name__)).info("Wrapped!")
            return func(*args, **kwargs)

        return wrapped


    # log = 'I am very like a linux pipe' | xfunc1 | xfunc2
    # logger.info(log)
    #
    # logger = logger.patch(lambda r: r.update(name=__file__, function=''))  # main:module
    # logger.info(log)
    #
    # # logger = logger.patch(wrapper(lambda x: ''))
    # # logger.info(log)

    ['aaaa', 'vvvvv'] | xprint


    def single(a):
        """ 定义一个简单的函数  """
        time.sleep(1)


    with timer('并行'):
        range(10) | xJobs(single)
