# -*- coding: utf-8 -*-
'''
从openweather网站提供的API接口获取城市当前气候数据
'''
# @Time    : 2022/11/30 11:35
# @Author  : LINYANZHEN
# @File    : get_weather_data.py
import requests, json, sys

# 高德天气api key
api_key = "de7c1290f77d0871b4448684cdeedefc"
# 纬度
latitude = "22.12"
# 经度
longitude = "113.52"

if __name__ == '__main__':
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    key = 'de7c1290f77d0871b4448684cdeedefc'
    # 嘉模堂区 820006
    data = {'key': key, "city": 820006}
    req = requests.post(url, data)
    info = dict(req.json())
    info = dict(info)
    print(info)
    newinfo = info['lives'][0]
    # print(newinfo)
    print("你查询的当地天气信息如下：")
    print("省市：", newinfo['province'] + newinfo['city'])
    print("城市：", newinfo['city'])
    print("编码：", newinfo['adcode'])
    print("天气：", newinfo['weather'])
    print("气温：", newinfo['temperature'] + '℃')
    print("风向：", newinfo['winddirection'])
    print("风力：", newinfo['windpower'])
    print("湿度：", newinfo['humidity'])
    print("报告时间：", newinfo['reporttime'])
