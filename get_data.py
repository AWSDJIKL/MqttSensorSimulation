# -*- coding: utf-8 -*-
'''
从服务器上获取遥测数据
'''
# @Time : 2022/11/29 10:11
# @Author : LINYANZHEN
# @File : get_data.py
from datetime import datetime
import tb_api
import pandas as pd

url = "http://118.190.148.75:8080"
# Default Tenant Administrator credentials
username = "1164958808@qq.com"
password = "xiaoHAO123ER"


def convert_13bit_unix_timestamp(timestamp):
    unix_ts = timestamp[:10]
    dt = datetime.fromtimestamp(float(unix_ts))
    return dt


tbapi = tb_api.TbApi(url, username, password)
device = tbapi.get_device_by_id("3e80da20-6bc3-11ed-83f6-cd76e8b0f552")
all_CO2 = tbapi.get_telemetry(device, "CO2")  # Lots more options on this method
print(all_CO2)
df=pd.DataFrame(all_CO2["CO2"])
print(df)