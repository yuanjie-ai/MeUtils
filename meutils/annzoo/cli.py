#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : ann
# @Time         : 2021/2/1 4:12 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : mi-ann --conf zk_path
# mongo id mapping

from meutils.pipe import *
from meutils.db.mongo import Mongo
from annzoo.ann import ANN

parser = argparse.ArgumentParser(description='ANN Serive')
parser.add_argument('--conf', default='/push/easyann/user_ann', help='zk/yaml')
args = parser.parse_args()

logger.info(f'cli args: {args.__dict__}')


class Config(BaseConfig):
    data = '/Users/yuanjie/Desktop/vec.parquet'
    reader = ''

    ips: List[str]
    collection_name = 'demo'
    ann_fields: List = Field([], alias='fields')
    auto_id: bool = True
    segment_row_limit: int = 4096
    batch_size = 10000

    # idmapping
    insert_vector: bool = False


conf = Config.parse_yaml(args.conf) if Path(args.conf).is_file() else Config.parse_zk(args.conf)


def insert_data(ip):
    ann = ANN(ip)
    ann.create_collection(
        conf.collection_name,
        fields=conf.ann_fields,
        auto_id=conf.auto_id,
        segment_row_limit=conf.segment_row_limit
    )

    dfs = eval(conf.reader)(conf.data)  # df生成器

    for df in dfs:
        ann_collection = ann.__getattr__(conf.collection_name)
        ids = ann_collection.batch_insert(df, conf.batch_size)

        if 'sid' in df:  # 无sid无需映射

            df['id'] = ids
            df['date'] = datetime.datetime.utcnow()  # ttl

            cols = ['id', 'sid', 'date'] + ['vec'] if conf.insert_vector else []  # 测试性能

            mongo_collection = Mongo(url=None).db.__getattr__(conf.collection_name)
            mongo_collection.insert_many(df[cols].to_dict('r'), False)


def main():
    conf.ips | xThreadPoolExecutor(insert_data, max_workers=3) | xlist


if __name__ == '__main__':
    main()
