#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : pipe_utils
# @Time         : 2020/11/12 11:35 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

from meutils.common import *


class Pipe(object):
    """I am very like a linux pipe"""

    def __init__(self, function):
        self.function = function
        functools.update_wrapper(self, function)

    def __ror__(self, other):
        return self.function(other)

    # def __call__(self, *args, **kwargs):
    #     return Pipe(lambda x: self.function(x, *args, **kwargs))
    def __call__(self, *args, **kwargs):
        return Pipe(
            lambda iterable, *args2, **kwargs2: self.function(
                iterable, *args, *args2, **kwargs, **kwargs2
            )
        )


########### 常用管道函数
# 进度条
xtqdm = Pipe(lambda iterable, desc=None: tqdm(iterable, desc))

# base types
xtuple, xlist, xset = Pipe(tuple), Pipe(list), Pipe(set)
xarray = Pipe(lambda x, decimals=None: np.array(x) if decimals is None else np.round(np.array(x), decimals))

# 高阶函数
xmap = Pipe(lambda iterable, func: map(func, iterable))
xmap_ = Pipe(lambda iterable, func: list(map(func, iterable)))

xzip = Pipe(lambda iterable, ismax=None: zip(*iterable) if ismax is None else itertools.zip_longest(*iterable))
xzip_ = Pipe(
    lambda iterable, ismax=None: list(zip(*iterable)) if ismax is None else list(itertools.zip_longest(*iterable)))

xreduce = Pipe(lambda iterable, func: reduce(func, iterable))

xfilter = Pipe(lambda iterable, func=None: filter(func, iterable))
xfilter_ = Pipe(lambda iterable, func=None: list(filter(func, iterable)))
# xtake = Pipe(lambda iterable, func=None: itertools.takewhile(func, iterable))
# xtake_ = Pipe(lambda iterable, func=None: list(itertools.takewhile(func, iterable)))
xdrop = Pipe(lambda iterable, func=None: itertools.dropwhile(func, iterable))
xdrop_ = Pipe(lambda iterable, func=None: list(itertools.dropwhile(func, iterable)))

# itertools: https://blog.csdn.net/weixin_43193719/article/details/87536371
xchain = Pipe(lambda iterable: itertools.chain(*iterable))
xchain_ = Pipe(lambda iterable: list(itertools.chain(*iterable)))

xenumerate = Pipe(lambda iterable, start=0: enumerate(iterable, start))
xenumerate_ = Pipe(lambda iterable, start=0: enumerate(iterable, start))

xshuffle = Pipe(lambda l, n_samples=None: sklearn.utils.shuffle(l, n_samples=n_samples))

# dateframe dfs
"""多个df: 
dfs = (
    Path('.').glob('demo*.txt') | xmap(lambda p: pd.read_csv(p, chunksize=2, names=['id'])) | xchain
)
"""
xconcat4df = Pipe(
    lambda dfs, convert_func=lambda x: x, axis=0: pd.concat(map(convert_func, dfs), ignore_index=True, axis=axis))

# str
xprint = Pipe(lambda s, sep='\n': print(s, sep=sep))
xjoin = Pipe(lambda chars, sep=' ': sep.join(map(str, chars)))
xsort = Pipe(lambda iterable, reverse=False: sorted(iterable, reverse=reverse))
xitemgetter = Pipe(lambda keys, dic: operator.itemgetter(*keys)(dic))
xstartswith = Pipe(lambda iterable, prefix=('_', '__', '.'): filter(lambda p: p.startswith(prefix)))
xendswith = Pipe(lambda iterable, suffix=('_', '__', '.'): filter(lambda p: p.startswith(suffix)))

# 统计词频
xCounter = Pipe(lambda iterable: Counter(iterable))


@Pipe
def xCounterUpdate(iterable, counter: Counter = None):
    """[['w1', 'w2'], ...]"""
    counter = counter or Counter()
    for i in iterable:
        counter.update(i)
    return counter


# operator: 排序、取多个值     https://blog.csdn.net/u010339879/article/details/98304292
# operator.itemgetter(*keys)(dic)


@Pipe
def xgetitem(iterable, index=0):
    """

    @param iterable: [(0, 1), (1, 2)] | xgetitem
    @param index:
    @return:
    """
    for i in iterable:
        yield operator.getitem(i, index)


# np
xstack = Pipe(lambda iterable, axis=0: np.stack(iterable, axis=axis))
xrow_stack = Pipe(lambda iterable, axis=0: np.row_stack(iterable))

# 调试用
xnext = Pipe(lambda ls: iter(ls).__next__())


@Pipe
def xwrite(iterable, filename):
    with open(filename, mode='a') as f:
        for line in iterable:
            f.write(f"{line}\n")


@Pipe
def xUnique(iterable, keep_order=True):
    if keep_order:
        return list(OrderedDict.fromkeys(iterable))  # 移除列表中的重复元素(保持有序)
    else:
        return list(set(iterable))


@Pipe
def xUnique_plus(iterable, key_fn: Callable = None):
    from joblib.hashing import hash
    hash_dict = {}

    for element in iterable:
        if key_fn:
            key = key_fn(element)
        else:
            key = element
        hash_dict[hash(key)] = element
    return list(hash_dict.values())


@Pipe
def xBloomFilter(iterable, bloom=None):
    """
        def bloom_add(iterable):
        bloom = pkl_load('bloom')
        for i in iterable:
            bloom.add(i)
        pkl_dump(bloom, 'bloom')
    """
    from pybloom_live import ScalableBloomFilter, BloomFilter
    bloom = bloom or ScalableBloomFilter(10 ** 6)
    for i in iterable:
        bloom.add(i)
    return bloom


@Pipe
def xbar4iter(iterable: list, func, batch_size=1, show_bar=True) -> list:
    """func 入参出参都是 list"""
    l = []
    _ = iterable | xgroup(batch_size)
    if show_bar: _ = tqdm(_)
    for i in _:
        l += func(i)
    return l


@Pipe
def xgroup(iterable, step=3, bins=None):
    n = len(iterable)
    if bins:
        step = max(n // bins, 1)

    _ = [iterable[idx: idx + step] for idx in range(0, n, step)]

    # if len(bins) > bins:  # todo: 确保正确的bins

    return _


@Pipe
def xsections(iterable, batch_size=3):
    def generator():
        yield from iterable

    g = generator()

    while True:
        group = list(itertools.islice(g, batch_size))
        if not group:
            break
        yield group


@Pipe
def xHashBins(ls, bins=3):
    """hash分组"""
    dic = {}
    for v in ls:
        dic.setdefault(murmurhash(v, bins=bins), []).append(v)
    return list(dic.values())


@Pipe
def xJobs(iterable, func, n_jobs=3):
    """支持匿名函数"""
    if n_jobs > 1:
        delayed_function = joblib.delayed(func)
        return joblib.Parallel(n_jobs=n_jobs)(delayed_function(arg) for arg in iterable)
        # yield from joblib.Parallel(n_jobs=n_jobs)(delayed_function(arg) for arg in iterable)
    else:
        return list(map(func, iterable))


@Pipe
def xThreadPoolExecutor(iterable, func, max_workers=5, desc="Processing", unit="it"):
    if max_workers > 1:
        with ThreadPoolExecutor(max_workers) as pool, tqdm(total=len(list(iterable)), desc=desc, unit=unit) as pbar:
            for i in pool.map(func, iterable):
                yield i
                pbar.update()

    else:
        return map(func, iterable)


@Pipe
def xProcessPoolExecutor(iterable, func, max_workers=5, desc="Processing", unit="it"):
    if max_workers > 1:
        with ProcessPoolExecutor(max_workers) as pool, tqdm(total=len(list(iterable)), desc=desc, unit=unit) as pbar:
            for i in pool.map(func, iterable):
                yield i
                pbar.update()

    else:
        return map(func, iterable)


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

# s = pd.DataFrame(range(10), columns=['a']).a
# idxs = np.where(s.isin((3, 6)))[0]
# ss = pd.cut(dd.a, [-np.inf, *idxs, np.inf])
# ss.groupby(ss).groups
