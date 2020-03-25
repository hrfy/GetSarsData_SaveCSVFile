# -*- coding: utf-8 -*-
# Version    : 1.0
# Time       : 2020/3/25
# Environment: python3.0
# Packages   : pandas, JSON, requests
# 导入模块
import json
import requests
import pandas as pd
import csv

# 抓取数据
## 先把数据都爬下来，查看数据结构，明确要整理保存的数据
def catch_data1():
    # url_1包含中国各省市当日实时数据(也有全球数据，但是腾讯改版后好久没更新了)
    url_1 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    response = requests.get(url=url_1).json()
    data_1 = json.loads(response['data'])
    return data_1
data_china = catch_data1()

def catch_data2():
    # url_2包含全球实时数据及历史数据、中国历史数据及每日新增数据
    url_2 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
    data_2 = json.loads(requests.get(url=url_2).json()['data'])
    return data_2
data_world = catch_data2()

lastUpdateTime = data_china["lastUpdateTime"]   # 腾讯最近更新时间
directory = ""                                  # 定义数据保存路径

# 获取中国当日实时数据
china_data = data_china["areaTree"][0]["children"]
## 获取中国各城市当日实时数据
filename = directory + lastUpdateTime.split(' ')[0] + "_china_city_data.csv"
with open(filename, "w+", encoding="utf_8_sig", newline="") as csv_file:
    writer = csv.writer(csv_file)
    header = ["province", "city_name", "total_confirm", "total_suspect", "total_dead", "total_heal",
              "today_confirm", "lastUpdateTime"]
    writer.writerow(header)
    for j in range(len(china_data)):
        province = china_data[j]["name"]  # 省份
        city_list = china_data[j]["children"]  # 该省份下面城市列表
        for k in range(len(city_list)):
            city_name = city_list[k]["name"]  # 城市名称
            total_confirm = city_list[k]["total"]["confirm"]  # 总确诊病例
            total_suspect = city_list[k]["total"]["suspect"]  # 总疑似病例
            total_dead = city_list[k]["total"]["dead"]  # 总死亡病例
            total_heal = city_list[k]["total"]["heal"]  # 总治愈病例
            today_confirm = city_list[k]["today"]["confirm"]  # 今日确诊病例
            data_row = [province, city_name, total_confirm, total_suspect, total_dead,
                        total_heal, today_confirm, lastUpdateTime]
            writer.writerow(data_row)
## 获取中国各省当日实时数据
filename = directory + lastUpdateTime.split(' ')[0] + "_china_province_data.csv"
with open(filename, "w+", encoding="utf_8_sig", newline="") as csv_file:
    writer = csv.writer(csv_file)
    header = ["province", "total_confirm", "total_suspect", "total_dead", "total_heal",
              "today_confirm", "lastUpdateTime"]
    writer.writerow(header)
    for i in range(len(china_data)):
        province = china_data[i]["name"]  # 省份
        total_confirm = china_data[i]["total"]["confirm"]  # 总确诊病例
        total_suspect = china_data[i]["total"]["suspect"]  # 总疑似病例
        total_dead = china_data[i]["total"]["dead"]  # 总死亡病例
        total_heal = china_data[i]["total"]["heal"]  # 总治愈病例
        today_confirm = china_data[i]["today"]["confirm"]  # 今日确诊病例
        data_row = [province, total_confirm, total_suspect, total_dead, total_heal, today_confirm, lastUpdateTime]
        writer.writerow(data_row)

# 获取中国历史数据及每日新增数据
chinaDayList = pd.DataFrame(data_world["chinaDayList"])  # 中国历史数据
filename = directory + lastUpdateTime.split(' ')[0] + "_china_history_data.csv"
header = ["date", "confirm", "suspect", "dead", "heal", "nowConfirm", "nowSevere", "deadRate", "healRate"]
chinaDayList = chinaDayList[header]  # 重排数据框列的顺序
chinaDayList.to_csv(filename, encoding="utf_8_sig", index=False)

chinaDayAddList = pd.DataFrame(data_world["chinaDayAddList"])  # 中国每日新增数据
filename = directory + lastUpdateTime.split(' ')[0] + "_china_DayAdd_data.csv"
header = ["date", "confirm", "suspect", "dead", "heal", "deadRate", "healRate"]
chinaDayAddList = chinaDayAddList[header]  # 重排数据框列的顺序
chinaDayAddList.to_csv(filename, encoding="utf_8_sig", index=False)

# 湖北与非湖北历史数据
def get_data_1():
    with open(filename, "w+", encoding="utf_8_sig", newline="") as csv_file:
        writer = csv.writer(csv_file)
        header = ["date", "dead", "heal", "nowConfirm", "deadRate", "healRate"]  # 定义表头
        writer.writerow(header)
        for i in range(len(hubei_notHhubei)):
            data_row = [hubei_notHhubei[i]["date"], hubei_notHhubei[i][w]["dead"], hubei_notHhubei[i][w]["heal"],
                        hubei_notHhubei[i][w]["nowConfirm"], hubei_notHhubei[i][w]["deadRate"],
                        hubei_notHhubei[i][w]["healRate"]]
            writer.writerow(data_row)

hubei_notHhubei = data_world["dailyHistory"]  # 湖北与非湖北历史数据
for w in ["hubei", "notHubei"]:
    filename = directory + lastUpdateTime.split(' ')[0] + "_" + w + "_history_data.csv"
    get_data_1()

# 获取湖北省与非湖北每日新增数据
hubei_DayAdd = pd.DataFrame(data_world["dailyNewAddHistory"])  # 中国历史数据
filename = directory + lastUpdateTime.split(' ')[0] + "_hubei_notHubei_DayAdd_data.csv"
hubei_DayAdd.to_csv(filename, encoding="utf_8_sig", index=False)

# 获取武汉与非武汉每日新增数据
wuhan_DayAdd = data_world["wuhanDayList"]
filename = directory + lastUpdateTime.split(' ')[0] + "_wuhan_notWuhan_DayAdd_data.csv"
with open(filename, "w+", encoding="utf_8_sig", newline="") as csv_file:
    writer = csv.writer(csv_file)
    header = ["date", "wuhan", "notWuhan", "notHubei"]  # 定义表头
    writer.writerow(header)
    for i in range(len(wuhan_DayAdd)):
        data_row = [wuhan_DayAdd[i]["date"], wuhan_DayAdd[i]["wuhan"]["confirmAdd"],
                    wuhan_DayAdd[i]["notWuhan"]["confirmAdd"], wuhan_DayAdd[i]["notHubei"]["confirmAdd"], ]
        writer.writerow(data_row)

# 全球实时数据及历史数据
## 获取全球各地区实时数据
global_data = data_world["foreignList"]
filename = directory + lastUpdateTime.split(' ')[0] + "_global_data.csv"
with open(filename, "w+", encoding="utf_8_sig", newline="") as csv_file:
    writer = csv.writer(csv_file)
    header = ["country", "date", "total_confirm", "total_suspect", "total_dead", "total_heal",
              "today_confirm", "lastUpdateTime"]
    writer.writerow(header)
    # 先写入中国的数据
    chinadate = lastUpdateTime.split(' ')[0][5:10].replace('-', '.')
    chinaData = ["中国", chinadate, data_china["chinaTotal"]["confirm"], data_china["chinaTotal"]["suspect"],
                 data_china["chinaTotal"]["dead"], data_china["chinaTotal"]["heal"],
                 data_china["chinaAdd"]["confirm"], lastUpdateTime]
    writer.writerow(chinaData)
    # 再写入其他国家地区的数据
    for i in range(len(global_data)):
        country = global_data[i]["name"]  # 国家或地区
        date = global_data[i]["date"]  # 日期
        total_confirm = global_data[i]["confirm"]  # 总确诊病例
        total_suspect = global_data[i]["suspect"]  # 总疑似病例
        total_dead = global_data[i]["dead"]  # 总死亡病例
        total_heal = global_data[i]["heal"]  # 总治愈病例
        today_confirm = global_data[i]["confirmAdd"]  # 今日确诊病例
        data_row = [country, date, total_confirm, total_suspect, total_dead, total_heal, today_confirm, lastUpdateTime]
        writer.writerow(data_row)
## 出于需要，转换一下英文名
## 世界各国中英文对照Chinese_to_English.xlsx下载于百度百科，自己添加了“日本本土”和“钻石号邮轮”的英文名，不然merge不出来。
world_name = pd.read_excel("Chinese_to_English.xlsx", sep='\t', encoding="utf-8")
globaldata = pd.read_csv(filename, encoding="utf_8_sig")
globaldata = pd.merge(globaldata, world_name, left_on="country", right_on="中文", how="inner")
header = ["country", "英文", "date", "total_confirm", "total_suspect", "total_dead", "total_heal",
          "today_confirm", "lastUpdateTime"]
globaldata = globaldata[header]
globaldata.to_csv(filename, encoding="utf_8_sig", index=False)

## 获取全球历史数据(除中国以外的总量)
globalDailyHistory = data_world["globalDailyHistory"]
filename = directory + lastUpdateTime.split(' ')[0] + "_globalDailyHistory.csv"
with open(filename, "w+", encoding="utf_8_sig", newline="") as csv_file:
    writer = csv.writer(csv_file)
    header = ["date", "total_dead", "total_heal", "newAddConfirm"]
    writer.writerow(header)
    for i in range(len(globalDailyHistory)):
        date = globalDailyHistory[i]["date"]  # 日期
        total_dead = globalDailyHistory[i]["all"]["dead"]  # 总死亡病例
        total_heal = globalDailyHistory[i]["all"]["heal"]  # 总治愈病例
        newAddConfirm = globalDailyHistory[i]["all"]["newAddConfirm"]  # 今日确诊病例
        data_row = [date, total_dead, total_heal, newAddConfirm]
        writer.writerow(data_row)

## 获取全球总量实时数据(中国以外)
globalNow = data_world["globalStatis"]
filename = directory + lastUpdateTime.split(' ')[0] + "_globalNow.csv"
with open(filename, "w+", encoding="utf_8_sig", newline="") as csv_file:
    writer = csv.writer(csv_file)
    header = ["nowConfirm", "confirm", "heal", "dead", "lastUpdateTime"]
    writer.writerow(header)
    data_row = [globalNow["nowConfirm"], globalNow["confirm"], globalNow["heal"], globalNow["dead"], lastUpdateTime]
    writer.writerow(data_row)

# 获取韩国、意大利、日本本土各城市当日实时数据
global_data = data_world["foreignList"]
dictt = {"韩国": "Korea", "意大利": "Italy", "日本本土": "Japan"}
for j in dictt.keys():
    filename = directory + lastUpdateTime.split(' ')[0] + "_" + dictt[j] + "_city_data.csv"
    with open(filename, "w+", encoding="utf_8_sig", newline="") as csv_file:
        writer = csv.writer(csv_file)
        header = ["country", "city_name", "date", "nameMap", "total_confirm", "total_suspect", "total_dead",
                  "total_heal", "confirmAdd", "lastUpdateTime"]
        writer.writerow(header)
        for k in range(len(global_data)):
            if global_data[k]["name"] == j:
                city_list = global_data[k]["children"]  # 该国家下面城市列表
                for h in range(len(city_list)):
                    city_name = city_list[h]["name"]  # 城市中文名
                    date = city_list[h]["date"]  # 日期
                    nameMap = city_list[h]["nameMap"]  # 城市英文名
                    total_confirm = city_list[h]["confirm"]  # 总确诊病例
                    total_suspect = city_list[h]["suspect"]  # 总疑似病例
                    total_dead = city_list[h]["dead"]  # 总死亡病例
                    total_heal = city_list[h]["heal"]  # 总治愈病例
                    confirmAdd = city_list[h]["confirmAdd"]  # 新增确诊病例
                    data_row = [j, city_name, date, nameMap, total_confirm, total_suspect, total_dead, total_heal,
                                confirmAdd, lastUpdateTime]
                    writer.writerow(data_row)
