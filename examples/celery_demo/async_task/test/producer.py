# 生产者
from fastapi import FastAPI
import requests
from pydantic import BaseModel

app = FastAPI()

task_url = "http://localhost:8501/celery/produce"
import pickle


# class RequestBody(BaseModel):
#     # returnUrl: str
#     data: dict
#     pipelines: list

# class RequestBody():
#     # returnUrl: str
#     data: dict
#     pipelines: list

def add(a, b):
    return a + b


def wedo(a):
    return a * 10


# @app.post("/produce")
# async def produce(request_body: RequestBody):
@app.get("/produce")
async def produce():
    # print(request_body.dict())
    # request_body.data = {
    #     "a": 10,
    #     "b": 20
    # }
    # request_body.list = [
    #     add, wedo
    # ]
    # print(request_body)

    # add = """lambda x:x+111"""
    add = r"""def add(x):
    return x+111"""
    # bbb = """lambda x:x+222"""
    bbb = r"""def bbb(x):
    return x+222"""

    json = {
        "data": 10,
        "pipelines": [
            add,
            bbb
        ]
    }
    print(json)
    # 发出20个请求
    response = requests.post(url=task_url, json=json)
    return {"code": 0, "data": response.json()}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8887)
