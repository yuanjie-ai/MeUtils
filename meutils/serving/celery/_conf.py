# 注意，celery4版本后，CELERY_BROKER_URL改为BROKER_URL
# https://www.yii666.com/article/344444.html

broker_url = 'amqp://username:passwd@host:port/虚拟主机名'

# 指定结果的接受地址

celery_result_backend = 'redis://username:passwd@host:port/db'

# 指定任务序列化方式 binary json msgpack

celery_task_serializer = 'msgpack'

# 指定结果序列化方式

celery_result_serializer = 'msgpack'

# 任务过期时间,celery任务执行结果的超时时间

celery_task_result_expires = 60 * 20

# 指定任务接受的序列化类型.

celery_accept_content = ["msgpack"]

# 任务发送完成是否需要确认，这一项对性能有一点影响

celery_acks_late = True

# 压缩方案选择，可以是zlib, bzip2，默认是发送没有压缩的数据

celery_message_compression = 'zlib'

# 规定完成任务的时间

celeryd_task_time_limit = 5  # 在5s内完成任务，否则执行该任务的worker将被杀死，任务移交给父进程

# celery worker的并发数，默认是服务器的内核数目,也是命令行-c参数指定的数目

celeryd_concurrency = 4

# celery worker 每次去rabbitmq预取任务的数量

celeryd_prefetch_multiplier = 4

# 每个worker执行了多少任务就会死掉，默认是无限的

celeryd_max_tasks_per_child = 40

# 设置默认的队列名称，如果一个消息不符合其他的队列就会放在默认队列里面，如果什么都不设置的话，数据都会发送到默认的队列中

celery_default_queue = "default"

# 设置详细的队列

celery_queues = {

    "default": {  # 这是上面指定的默认队列

        "exchange": "default",

        "exchange_type": "direct",

        "routing_key": "default"

    },

    "topicqueue": {  # 这是一个topic队列 凡是topictest开头的routing key都会被放到这个队列

        "routing_key": "topic.#",

        "exchange": "topic_exchange",

        "exchange_type": "topic",

    },

    "task_eeg": {  # 设置扇形交换机

        "exchange": "tasks",

        "exchange_type": "fanout",

        "binding_key": "tasks",

    },

}
