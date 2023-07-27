#!/usr/bin/env python
# coding: utf-8
from easydata import hive
import Levenshtein as lt

def edit_distance(df):
    res = lt.editops(df['asr_text'],df['smit_text'])
    distance = {'insert':0,'delete':0,'replace':0}
    for r in res:
        distance[r[0]]+=1
    df['insr_dist'] = distance['insert']
    df['del_dist'] = distance['delete']
    df['rep_dist'] = distance['replace']
    return df

if __name__ == '__main__':
    df = hive.read_hive_table('easyops-cluster','smartdata','tmp_dwd_evt_asr_jour_di_01','smartdata')
    df = df.reindex(columns=['user_no','user_nme','evt_tm','evt_dt','equp_tp','equp_mdl','asr_text','smit_text','insr_dist','del_dist','rep_dist'], fill_value=0)
    df = df.apply(lambda x:edit_distance(x),axis=1)
    hive.write_hive_table(df, "easyops-cluster", "smartdata","tmp_dwd_evt_asr_jour_di_02", queue_name="smartdata", mode="overwrite",store_type="parquet")
    print('done')