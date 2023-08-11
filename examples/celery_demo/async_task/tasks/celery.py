# 异步任务 消息队列
from celery import Celery
import requests
import pickle
import re

# broker = 'redis://:Yy251314@121.196.183.67:6379/1'  # 消息中间件 redis
# backend = 'redis://:Yy251314@121.196.183.67:6379/2'  # 结果存储 redis

# 创建 Celery 实例
# celery = Celery('tasks', broker=broker, backend=backend)
celery = Celery('tasks')
celery.config_from_object('tasks.celeryconfig')  # 引入配置文件
import json


# import datetime
# def extract_function_name(function_string):
#     pattern = r"def\s+(\w+)\s*\("
#     match = re.search(pattern, function_string)
#     if match:
#         return match.group(1)
#     return None
#
#
# def parse_code(code_str):
#     code_obj = compile(code_str, "<string>", "exec")
#     namespace = {}
#     exec(code_obj, namespace)
#     return namespace[extract_function_name(code_str)]


# 启动 Celery 的 Worker 进程：
# celery -A tasks.celery worker --loglevel=info
@celery.task
# def process_task(data, pipelines, fun1, fun2):
def process_task(data, pipelines):
    # print("fn_pkl", fn_pkl)
    #
    # fn = pickle.loads(fn_pkl)
    # print("fn", fn)
    # print(data)
    # print(pipelines)
    # 将要执行的任务逻辑写在这里
    # print(returnUrl)
    # print(data)
    # 获取当前日期和时间
    # current_time = datetime.now()
    # 将当前时间格式化为字符串
    # formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    # 输出当前日期和时间
    # print(formatted_time)

    # response = requests.post(url=returnUrl, json=data)
    # return f"url：{returnUrl} --> 结果：{response.json()}"
    # return f"{response.json()}"

    # 提取函数列表
    # pipelines = json.loads(pipelines)
    print("data", data)
    print("pipelines", pipelines)
    for pipeline in pipelines:
        # print(pipeline)
        # print(type(pipeline))
        # eval函数只能解析单行的表达式
        data = eval(pipeline)(data)
        # fun = parse_code(pipeline)
        # data = fun(data)

    return f"{data}"


