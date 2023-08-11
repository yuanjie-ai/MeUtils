# 异步任务 消息队列
import pickle

from fastapi import FastAPI
from pydantic import BaseModel
from celery.result import AsyncResult
from tasks.celery import process_task
from tasks.celery import celery


class RequestBody(BaseModel):
    pipelines: list
    # data: dict
    data: object


app = FastAPI()


# 启动fastapi应用
# uvicorn main:app --reload

@app.get("/")
async def root():
    return {"message": "Hello World"}


"""
生产者 -- 生产消息
访问该请求
将会启动一个异步的 Celery 任务，并返回任务 ID。Celery Worker 进程将会处理这个任务，执行相应的任务逻辑，并返回结果。
"""


@app.post("/celery/produce")
async def produce(request_body: RequestBody):
    # print(request_body.returnUrl)
    # print(request_body.data)
    # 启动异步任务
    result = process_task.delay(request_body.data, request_body.pipelines)
    # result = process_task.apply_async(args=[request_body.returnUrl, request_body.data],countdown=10)  # # 调用异步任务并设置时间间隔 10s
    return {"taskId": result.id}


# 查看异步任务的执行结果
@app.get("/celery/getTaskResult")
async def getResult(taskId):
    asyncResult = AsyncResult(id=taskId, app=celery)
    message = ""
    code = 500
    if asyncResult.successful():  # 正常执行完成
        result = asyncResult.get()  # 任务返回的结果
        code = 0
        message = result
    elif asyncResult.failed():
        message = "任务失败"
    elif asyncResult.status == 'PENDING':
        message = "任务等待中被执行"
    elif asyncResult.status == 'RETRY':
        message = "任务异常后正在重试"
    elif asyncResult.status == 'STARTED':
        message = "任务已经开始被执行"
    return {
        "code": code,
        "data": {
            "taskId": taskId,
            "message": message
        }}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8501)
