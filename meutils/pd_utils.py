#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : pd_utils
# @Time         : 2020/11/12 11:35 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

from sklearn.model_selection import StratifiedKFold, ShuffleSplit

from meutils.common import *
from meutils.decorators import deprecated


def df2dict(df):
    assert df.shape[1] == 2
    return dict(zip(*map(df.__getitem__, df.columns)))


def pd_bind(cls=pd.DataFrame, *funcs):
    for f in funcs:
        setattr(cls, f.__name__, f)


df_memory = lambda df, deep=False: df.memory_usage(deep=deep).sum() / 1024 ** 2


def df_kfold_split(df, label='target', cv=5, split_seed=42):
    """
        from sklearn.datasets import load_iris
        df = pd.concat(load_iris(return_X_y=True, as_frame=1), 1)
        for df_train, df_valid in df_kfold_split(df, 'target'):
            break

    @param df:
    @param label:
    @param cv:
    @param split_seed:
    @return:
    """
    if label in df:
        folds = StratifiedKFold(n_splits=cv, shuffle=True, random_state=split_seed).split(df, df[label])
    else:
        logger.info(f"{label} not in df")
        folds = ShuffleSplit(n_splits=cv, random_state=split_seed).split(df)  # todo: 兼容时间序列

    for train_index, valid_index in folds:
        yield df.iloc[train_index], df.iloc[valid_index]  # df_train, df_valid


def dfs_join_(dfs):
    return reduce(lambda left, right: pd.merge(left, right), dfs)


def dfs_join(df, dfs, keys_list=None):
    for df_, keys in tqdm(zip(dfs, keys_list), desc='joining🐢'):
        df = df.merge(df_, on=keys)
    return df


def df2json(df, filename='x.json'):
    df.to_json(filename, orient='records', lines=True)


def split(df, num_part=None, batch_size=None):
    assert any((num_part, batch_size)), "num_part, batch_size 不能同时为 None"

    if num_part is None:
        num_part = max(len(df) // batch_size, 1)

    yield from np.array_split(df, num_part)  # 仍保留原始索引


def duplicate_columns(frame):
    """keep='first' 
    https://stackoverflow.com/questions/14984119/python-pandas-remove-duplicate-columns/32961145#32961145
    数据大:
        dups = duplicate_columns(df)
        df.drop(dups, 1)

    数据小:
        df.T.drop_duplicates().T
    """
    frame = frame.fillna(-123456)  # 处理缺失值

    groups = frame.columns.to_series().groupby(frame.dtypes).groups
    dups = []
    for t, v in groups.items():
        dcols = frame[v].to_dict(orient="list")

        vs = list(dcols.values())
        ks = list(dcols.keys())
        lvs = len(vs)

        for i in range(lvs):
            for j in range(i + 1, lvs):
                if vs[i] == vs[j]:
                    dups.append(ks[j])  # keep='first'
                    break
    return dups


def reduce_mem_usage(df):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024 ** 2
    for col in tqdm(df.columns, desc="Reduce memory"):
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        # else:
        #     df[col] = df[col].astype('category')

    end_mem = df.memory_usage().sum() / 1024 ** 2
    print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))

    return df


def to_html_plus(df, title='Title', subtitle='Subtitle'):
    from jinja2 import Environment, PackageLoader
    env = Environment(loader=PackageLoader('meutils'))
    template = env.get_template('df_html.j2')

    content = template.render(df_to_html=df.to_html(), title=title, subtitle=subtitle)
    # with open('./df.html', 'w') as fp:
    #     fp.write(content)
    return content


def to_compress(df: pd.DataFrame, filename, method='zip', archive_name='data.csv', index=False, **to_csv_kwargs):
    """

    @param df:
    @param method: mode is one of {{'infer', 'gzip', 'bz2', 'zip', 'xz', None}}
    @param archive_name:
    @return:
    """
    to_csv_kwargs['index'] = index
    to_csv_kwargs['compression'] = dict(method=method, archive_name=archive_name)
    df.to_csv(filename, **to_csv_kwargs)


# 绑定到pandas
dataframe_funcs = [
    to_compress,
    split
]
pd_bind(pd.DataFrame, *dataframe_funcs)

if __name__ == '__main__':
    # df = pd.DataFrame([[1, 2, 3] * 10000, [2, 2, 3] * 10000, [3, 2, 3] * 10000])
    #
    # import time
    #
    # s = time.time()
    # reduce_mem_usage(df)  # 34
    #
    # print(time.time() - s)
    from jinja2 import Template, Environment, PackageLoader, FileSystemLoader

    # env = Environment(loader=FileSystemLoader('./'))
    env = Environment(loader=PackageLoader('meutils'))
    template = env.get_template('df_html.j2')

    df = pd.DataFrame(range(10))
    content = template.render(df_to_html=df.to_html(), title="title", subtitle='subtitle')

    print(content)

    with open('./df.html', 'w') as fp:
        fp.write(content)
