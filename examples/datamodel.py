#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : datamodel
# @Time         : 2020/12/2 10:34 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 

"""Optional[X]等价于Union[X, None]

Union 是当有多种可能的数据类型时使用
Optional 是Union的一个简化， 当 数据类型中有可能是None时，比如有可能是str也有可能是None，则Optional[str], 相当于Union[str, None]
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ValidationError


class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: datetime = None
    friends: List[int] = []
    x: Optional[int] = None


# 正确调用
user = User(id=1, name='XerCis', signup_ts='2020-05-20 13:14', friends=[1, 2, 3])
print(user.id)
print(user.signup_ts)
print(user.friends)

# 错误调用
try:
    User(signup_ts='not datetime', friends=[1, 2, 'not int'])
except ValidationError as e:
    print(e.json())
