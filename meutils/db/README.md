# DB

## Redis
队列
http://www.coolpython.net/python_db/redis/py-redis-queue.html
## MongoDB
# https://www.jb51.net/article/159652.htm
# https://www.cnblogs.com/kaituorensheng/p/5181410.html
"""
 # info
 collection.count_documents({})

 # 增
 collection.insert_one({'x': 1})
 collection.insert_one({'xx': 2})
 ids = collection.insert_many([{'xxx': 3}, {'xxx': 4}])

 from bson.objectid import ObjectId

 collection.find_one({'x': 1})
 collection.find_one({'_id': ObjectId('5e743cea06be472ac7298def')})

 # 复杂的查询
 list(collection.find({})) # collection.find().count()
 list(collection.find({'xx': {'$gt': 1}}))

 condition = {'s': 1}
 # update_one update_many
 # result = collection.replace_one(condition, {'s': 1, 'ss': 2}) # 完全替换 # upsert=True强拆
 result = collection.replace_one(condition, {'$set': {'s':1, 'sss': 3}}) # {**d1, **d2}
"""
"""插入速度200维向量 20w/min
    tag2vec = m.db.word2vec.tag2vec
    tag2vec.delete_many({})
    tag2vec.count_documents({})
    docs = get_docs(dff.w, dff.v)
    tag2vec.insert_many(docs, False)
    tag2vec.find_one()
    tag2vec.count_documents({})

    # https://www.cnblogs.com/wangyuxing/p/9879504.html
    news_word2vec.find_one({'id': 0}, projection={'v': 0}) # 指定返回键值
    tag2vec.find({'w': {'$in': ['娱乐', '体育']}}) # $in $nin

    l = [{'w': 1, 'v': 2}, {'w': 3, 'v': 4}]
    dic = dict([i.values() for i in l])
    [{'w': k, 'v': v} for k, v in dic.items()]

    collection.insert_many(docs, False)

    """