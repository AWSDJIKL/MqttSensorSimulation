# -*- coding: utf-8 -*-
'''
工具函数
'''
# @Time    : 2022/11/30 10:25
# @Author  : LINYANZHEN
# @File    : utils.py
from datetime import datetime
import time


def timestamp_to_datetime(timestamp):
    '''
    将13位的unix时间戳转换为datetime

    :param timestamp:
    :return:
    '''
    timestamp = str(timestamp)
    unix_ts = timestamp[:10]
    dt = datetime.fromtimestamp(float(unix_ts))
    return dt


def now_to_timestamp(time):
    '''
    将当前时间转换为13位的unix时间戳

    :param time:
    :return:
    '''
    return int(round(time.time()) * 1000)
