# -*- coding: utf-8 -*-
'''
模拟设备发送遥测数据
'''
# @Time : 2022/11/29 9:53
# @Author : LINYANZHEN
# @File : sent_data.py
from paho.mqtt import client as mqtt
import time

device_token = ["EoRwQj29lbmewzeU2JmR",
                "QgIlpTywhvPEMrJ65nzX"]


def on_connect(client, userdata, flags, rc):
    """一旦连接成功, 回调此方法"""
    rc_status = ["连接成功", "协议版本错误", "无效的客户端标识", "服务器无法使用", "用户名或密码错误", "无授权"]
    print("connect：", rc_status[rc])


def mqtt_connect():
    """连接MQTT服务器"""
    client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    mqttClient = mqtt.Client(client_id)
    mqttClient.on_connect = on_connect  # 返回连接状态的回调函数
    MQTTHOST = "118.190.148.75"  # MQTT服务器地址
    MQTTPORT = 1883  # MQTT端口
    mqttClient.username_pw_set(device_token[1])  # mqtt服务器账号密码
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()  # 启用线程连接

    return mqttClient


# 发布消息
def mqtt_publish():
    """发布主题为'mqtt/demo',内容为'Demo text',服务质量为2"""
    mqttClient = mqtt_connect()
    text = "{\"key\":\"101\"}"
    mqttClient.publish('v1/devices/me/telemetry', text, 2)
    print("send")
    disconnect(mqttClient)


def disconnect(mqttClient):
    mqttClient.loop_stop()
    mqttClient.disconnect()
    print("disconnect")


if __name__ == '__main__':
    mqtt_publish()
