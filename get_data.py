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
import utils

url = "http://118.190.148.75:8080"
# Default Tenant Administrator credentials
username = "1164958808@qq.com"
password = "xiaoHAO123ER"
columns = ["Temp", "CO2", "Hum", "Light", "PM2_5"]
device_id = "3e80da20-6bc3-11ed-83f6-cd76e8b0f552"

def convert_13bit_unix_timestamp(timestamp):
    unix_ts = timestamp[:10]
    dt = datetime.fromtimestamp(float(unix_ts))
    return dt


if __name__ == '__main__':
    tbapi = tb_api.TbApi(url, username, password)
    device = tbapi.get_device_by_id(device_id)
    all_data = tbapi.get_telemetry(device, columns)  # Lots more options on this method
    print(all_data)
    dfs = []
    for column in columns:
        df = pd.DataFrame(all_data[column])
        df = df.rename(columns={"ts": "time", "value": column})
        dfs.append(df)
    df = dfs[0]
    for i in range(1, len(columns)):
        df = pd.merge(df, dfs[i])
    # 将时间戳转换为datetime
    df["time"] = df["time"].apply(utils.timestamp_to_datetime)
    print(df)
    # 保存为csv
