https://github.com/pypa/pyproject-hooks/blob/main/pyproject.toml
https://github.com/tox-dev/pyproject-fmt


# 子粒度缓存
from meutils.pipe import *
from joblib import hashing

@decorator
def diskcache4list(func, location='cachedir', ttl=None, *args, **kwargs):

    from diskcache import Cache, FanoutCache

    cache = Cache(directory=location)
    cache.set = partial(cache.set, expire=ttl)
    
    @background_task
    def cache_set(k2v):
        for k, v in k2v.items():
            if cache.get(k) is None:
                logger.info(k)
                cache.set(k, v)
    
    batch = args[0]
    raw_k = hashing.hash(batch)
    _ = cache.get(raw_k)
    if _:
        print(11111)
        cache_set(dict(zip(batch, _)))
        return _
    
    ks = [] # 保持顺序
    hits = {}
    nohits = {}
    for _k in batch:
        k = hashing.hash([_k])
        ks.append(k)
        v = cache.get(k)
        if v is None:
            nohits[k] = _k
        else:
            hits[k] = v
            
    print(f'nohits: {nohits}')
    print(f'hits: {hits}')

    # 计算未命中的 key
    if nohits:
        batch = list(nohits.values())
        print(f"batch: {batch}")
        batch_v = list(func(batch))
        nohits = dict(zip(nohits, batch_v))
    
    # 合并结果
    k2v = {**hits, **nohits} 
    _  = [k2v[k] for k in ks] # 排序
     
    # 计入缓存
    nohits[raw_k] = _
    cache_set(nohits)
    return _


def f(x):
    time.sleep(1)
    return [f"{k}_{v}" for k, v in enumerate(x)]

@diskcache4list
def ff(x):
    time.sleep(1)
    return [f"{k}_{v}" for k, v in enumerate(x)]