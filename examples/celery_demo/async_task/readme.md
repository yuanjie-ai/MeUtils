异步任务：

异步队列 celery：app2.0 
    生产队列：暴露接口给调用方 放到 tasks【返回taskid】
消费：task兼容N个人任务【通过调用微服务】
结果：暴露接口，取结果【通过taskid获取信息】
取到
取不到
计算失败
pending
在计算

安装
pip install "fastapi[all]"
或者
pip install fastapi
pip install "uvicorn[standard]"

安装
pip install celery

运行项目 main是指main.py中的app
uvicorn main:app --reload
```
提示：uvicorn main:app 命令含义如下:
main：main.py 文件（一个 Python「模块」）。
app：在 main.py 文件中通过 app = FastAPI() 创建的对象。
--reload：让服务器在更新代码后重新启动。仅在开发时使用该
```

可以查看到swaggerUI接口文档
http://127.0.0.1:8000/docs

