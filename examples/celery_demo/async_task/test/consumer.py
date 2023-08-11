# 消费者
from fastapi import FastAPI, Request
import time
import asyncio
from datetime import datetime

app = FastAPI()


def getCurrentFormatTime():
    # 获取当前时间
    current_time = datetime.now()
    # 将当前时间格式化为字符串
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


@app.post("/consumer")
async def consumer(request: Request):
    try:
        # time.sleep(5)
        data = await request.json()
        # data = request.json()
        # time.sleep(10)
        print(getCurrentFormatTime(), "开始执行业务")
        await asyncio.sleep(30)
        print(getCurrentFormatTime(), "执行业务结束")

        print(getCurrentFormatTime(), data)
        # 在这里对接收到的数据进行处理
        # ...
        return {"message": "consumer 消息OK"}
    except Exception as e:
        return {"message": "请求发生错误"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8888)
