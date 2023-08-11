# celery的配置文件
broker_url = 'redis://:Yy251314@121.196.183.67:6379/1'  # 使用RabbitMQ作为消息代理
result_backend = 'redis://:Yy251314@121.196.183.67:6379/2'  # 把任务结果存在了Redis
result_serializer = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
worker_concurrency = 4  # 4个并发线程
result_expires = 60 * 60 * 24 * 30  # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显

task_default_retry_delay = 60  # 在任务失败后延迟60秒进行重试
task_default_max_retries = 3  # 任务的最大重试次数

result_encoding = 'utf-8'  # 设置结果编码为UTF-8
