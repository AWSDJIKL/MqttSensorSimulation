# -*- coding: utf-8 -*-
'''
和风天气，有空气质量
'''
# @Time    : 2022/11/30 20:15
# @Author  : LINYANZHEN
# @File    : qweather.py
import requests, json, sys
import pandas as pd


def get_weather_and_air(longitude, latitude):
    api_key = "3b5f528592454cccb530f76b4c0f0fd5"
    weather_url = "https://devapi.qweather.com/v7/weather/now?location={},{}&key={}".format(longitude, latitude,
                                                                                            api_key)
    air_url = "https://devapi.qweather.com/v7/air/now?location={},{}&key={}".format(longitude, latitude, api_key)
    weather_data = requests.get(weather_url).json()
    air_data = requests.get(air_url).json()
    return {
        "temp": weather_data["now"]["temp"],
        "humidity": weather_data["now"]["humidity"],
        "pressure": weather_data["now"]["pressure"],
        "pm10": air_data["now"]["pm10"],
        "pm2p5": air_data["now"]["pm2p5"],
        "no2": air_data["now"]["no2"],
        "so2": air_data["now"]["so2"],
        "co": air_data["now"]["co"],
        "o3": air_data["now"]["o3"],
    }


if __name__ == '__main__':
    # get_weather_and_air(113.5, 22.2)
    device_data = pd.read_csv("device_data.csv")
    api_key = "3b5f528592454cccb530f76b4c0f0fd5"
    for index, row in device_data.iterrows():
        city_name = row["device_name"]
        city_url = "https://geoapi.qweather.com/v2/city/lookup?location={}&key={}".format(city_name, api_key)
        data = requests.get(city_url).json()
        print(city_name)
        print(data)
        print("latitude:", data["location"][0]["lat"])
        print("longitude:", data["location"][0]["lat"])
        device_data.loc[index, "latitude"] = data["location"][0]["lat"]
        device_data.loc[index, "longitude"] = data["location"][0]["lon"]
