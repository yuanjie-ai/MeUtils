# 不错的库
[typer](typer_demo.py)

[rich](rich_demo.py)

[dearpygui](https://github.com/hoffstadt/DearPyGui)

[diagrams](https://diagrams.mingrammer.com/docs/guides/cluster)

[Hummingbird](https://github.com/microsoft/hummingbird): 部署


[alibi-detect](https://github.com/SeldonIO/alibi-detect)：
监控生产模型中的异常值和分布漂移，适用于表格数据、文本、图像和时间序列。

pytorch-forecasting：在现实世界的案例和研究中，利用神经网络简化时间序列预测。

sktime：提供专门的时间序列算法和 scikit-learn 兼容工具，用于构建、调整和评估复合模型。也可以查看他们的配套 sktime-dl 包，用于基于深度学习的模型。

pycaret：封装了几个常见的机器学习库，使工作效率大大提高，并节省了数百行代码。

stanza：来自斯坦福的 60 多种语言的精确自然语言处理工具。多种可用的预训练模型用于不同的任务。

einops：einops 在 2020 年普及，可以让你为可读和可靠的代码编写张量操作，支持 NumPy、PyTorch、TensorFlow 等。Karpathy 推荐的，你还需要什么吗？

HiPlot: 高维数据可视化# 不错的库

tabnet

dtale 数据分析/可输出代码


请求表单
```
from requests_toolbelt import MultipartEncoder
import requests

m = MultipartEncoder(fields={'field0': 'value', 'field1': 'value'})

r = requests.post('http://0.0.0.0:8000/x/title/yuanjie@xiaomi.com', data=m,
                  headers={'Content-Type': m.content_type})

```


内存debug工具 https://github.com/zhuyifei1999/guppy3















