[![Downloads](http://pepy.tech/badge/meutils)](http://pepy.tech/project/meutils)

## Install
```bash
pip install -U meutils
```

## Usages

### Logger
```python
from meutils.pipe import *

logger.add('run.log')

for i in range(5) | xtqdm:
    logger.info("这是一个进度条")

with timer('LOG'):
    logger.info("打印一条log所花费的时间")

```

### Tools
- debug: 在pysnooper基础上加了调试开关，默认开启调试
```python
# import os
# os.environ['debug'] = '0'
from meutils.pipe import debug
@debug()
def func():
    pass
func()
```

### Notice
```python
from meutils.pipe import *
from meutils.log_utils import logger4wecom
from meutils.decorators.catch import wecom_catch, wecom_hook

@wecom_catch()
def wecom_catch_test():
    1/0

@wecom_hook('wecom_hook_test', 'Sleeping 3s')
def wecom_hook_test():
    time.sleep(3)

```
### CLI
```bash
mecli pkg
```

---
## TODO


