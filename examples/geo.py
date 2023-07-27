#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : geo
# @Time         : 2021/1/24 12:57 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : https://mp.weixin.qq.com/s/OWxGhrqp-PQ1EF4Pj847Eg

import geopy
from geopy.geocoders import Nominatim

geolocator = geopy.geocoders.BaiduV3('maI6DOkOGSQwDYlh10GLVUq7lxdbFeX2')
location = geolocator.geocode("南京")
print(location.raw)

geolocator = Nominatim(user_agent="test_geo")
location = geolocator.geocode("南京")
print(location.raw)


# todo
# 行政区编码：https://mapopen-website-wiki.cdn.bcebos.com/cityList/weather_district_id.csv
# 天气：http://api.map.baidu.com/weather/v1/?district_id=320111&data_type=all&ak=maI6DOkOGSQwDYlh10GLVUq7lxdbFeX2