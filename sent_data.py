# -*- coding: utf-8 -*-
'''
模拟设备发送遥测数据
'''

# @Time : 2022/11/29 9:53
# @Author : LINYANZHEN
# @File : sent_data.py
from paho.mqtt import client as mqtt
import time
import pandas as pd
import tb_api
import requests

url = "http://118.190.148.75:8080"
# Default Tenant Administrator credentials
username = "1164958808@qq.com"
password = "xiaoHAO123ER"

data_column = ["temp", "humidity", "pressure", "pm10", "pm2p5", "no2", "so2", "co", "o3"]


#
# def on_connect(client, userdata, flags, rc):
#     """一旦连接成功, 回调此方法"""
#     rc_status = ["连接成功", "协议版本错误", "无效的客户端标识", "服务器无法使用", "用户名或密码错误", "无授权"]
#     print("connect：", rc_status[rc])
#
#
# def mqtt_connect():
#     """连接MQTT服务器"""
#     client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
#     mqttClient = mqtt.Client(client_id)
#     mqttClient.on_connect = on_connect  # 返回连接状态的回调函数
#     MQTTHOST = "118.190.148.75"  # MQTT服务器地址
#     MQTTPORT = 1883  # MQTT端口
#     mqttClient.username_pw_set(device_token[1])  # mqtt服务器账号密码
#     mqttClient.connect(MQTTHOST, MQTTPORT, 60)
#     mqttClient.loop_start()  # 启用线程连接
#
#     return mqttClient
#
#
# # 发布消息
# def mqtt_publish():
#     """发布主题为'mqtt/demo',内容为'Demo text',服务质量为2"""
#     mqttClient = mqtt_connect()
#     text = "{\"key\":\"101\"}"
#     mqttClient.publish('v1/devices/me/telemetry', text, 2)
#     print("send")
#     disconnect(mqttClient)
#
#
# def disconnect(mqttClient):
#     mqttClient.loop_stop()
#     mqttClient.disconnect()
#     print("disconnect")


def create_device():
    device_data = pd.read_csv("device_data.csv")
    # print(city_data)
    tbapi = tb_api.TbApi(url, username, password)
    for i in range(len(device_data)):
        city_name = device_data.loc[i, "device_name"]
        device = tbapi.add_device(device_data.loc[i, "device_name"], "python_sensor", None, None)
        longitude, latitude = get_city_data(city_name)
        device_data.loc[i, "device_id"] = tbapi.get_id(device)
        device_data.loc[i, "device_token"] = tbapi.get_device_token(device)
        device_data.loc[i, "longitude"] = longitude
        device_data.loc[i, "latitude"] = latitude
    print(device_data)
    device_data.to_csv("device_data.csv", index=False)


def get_city_data(city_name):
    api_key = "3b5f528592454cccb530f76b4c0f0fd5"
    city_url = "https://geoapi.qweather.com/v2/city/lookup?location={}&key={}".format(city_name, api_key)
    data = requests.get(city_url).json()
    return data["location"][0]["lon"], data["location"][0]["lat"]


def get_weather_and_air(longitude, latitude):
    weather_api_key = "3b5f528592454cccb530f76b4c0f0fd5"
    air_api_key = "1a409a4d6dfb4b4093c20517eb90f8f4"
    weather_url = "https://devapi.qweather.com/v7/weather/now?location={},{}&key={}".format(longitude, latitude,
                                                                                            weather_api_key)
    air_url = "https://devapi.qweather.com/v7/air/now?location={},{}&key={}".format(longitude, latitude, air_api_key)
    weather_data = requests.get(weather_url).json()
    # print(weather_data)
    air_data = requests.get(air_url).json()
    # print(air_data)
    return {
        "temp": float(weather_data["now"]["temp"]),
        "humidity": float(weather_data["now"]["humidity"]),
        "pressure": float(weather_data["now"]["pressure"]),
        "pm10": float(air_data["now"]["pm10"]),
        "pm2p5": float(air_data["now"]["pm2p5"]),
        "no2": float(air_data["now"]["no2"]),
        "so2": float(air_data["now"]["so2"]),
        "co": float(air_data["now"]["co"]),
        "o3": float(air_data["now"]["o3"]),
    }


def send_weather():
    device_data = pd.read_csv("device_data.csv")
    tbapi = tb_api.TbApi(url, username, password)
    for index, row in device_data.iterrows():
        print(row["device_name"])
        data = get_weather_and_air(longitude=row["longitude"], latitude=row["latitude"])
        print(data)
        data["longitude"] = row["longitude"]
        data["latitude"] = row["latitude"]
        tbapi.send_telemetry(device_token=row["device_token"], data=data)
        print("send")


if __name__ == '__main__':
    # mqtt_publish()
    # create_device()
    while True:
        send_weather()
        time.sleep(60 * 15)
