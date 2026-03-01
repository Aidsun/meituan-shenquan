#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# GitHub Actions 适配版 + 详细推送

import os
import sys
import json
import urllib.request
import ssl
import datetime

ssl._create_default_https_context = ssl._create_unverified_context

# 从环境变量读取配置
token = os.environ.get("token", "")
webhook = os.environ.get("webhook", "")
wm_latitude = os.environ.get("wm_latitude", "30657401")
wm_longitude = os.environ.get("wm_longitude", "104063321")
propId = int(os.environ.get("propId", "5"))
exchangeCoinNumber = int(os.environ.get("exchangeCoinNumber", "1800"))
setexchangedou = int(os.environ.get("setexchangedou", "1800"))
yesornot2 = os.environ.get("yesornot2", "n")

# 常量
parActivityId = "Gh1tkq-wvFU2xEP_ZPzHPQ"
wm_ctype = "mtandroid"
portraitId = 498
baseurl = "https://i.waimai.meituan.com"
head = {
    "Host": "i.waimai.meituan.com",
    "User-Agent": "MeituanGroup/11.9.208",
    "x-requested-with": "XMLHttpRequest",
    "content-type": "application/x-www-form-urlencoded"
}

# 日志收集器
class LogCollector:
    def __init__(self):
        self._buff = ""
    def write(self, message):
        self._buff += message
        sys.__stdout__.write(message)  # 同时输出到控制台
    def flush(self):
        sys.__stdout__.flush()

# 创建收集器并重定向 stdout
log_collector = LogCollector()
sys.stdout = log_collector

def signForBeans():
    print("**开始执行签到领豆脚本:**")
    datas = f"token={token}"
    url = baseurl + "/cfeplay/playcenter/batchgrabred/drawPoints/v2"
    req = urllib.request.Request(url, headers=head, data=datas.encode("utf-8"), method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read().decode("utf-8"))
        if result["code"] == 0:
            print("👴" + result["msg"])
        elif result["code"] == 1:
            print("👴未到领取时间或已领完")
        elif result["code"] == 7:
            print("token已失效")
        else:
            print("未知响应")
    except Exception as e:
        print(f"签到异常: {e}")

def doAction():
    print("**开始执行每日签到领必中符脚本:**")
    datas = f"parActivityId={parActivityId}&wm_latitude={wm_latitude}&wm_longitude={wm_longitude}&token={token}&action=SiginInGetProp"
    url = baseurl + "/cfeplay/playcenter/batchgrabred/doAction"
    req = urllib.request.Request(url, headers=head, data=datas.encode("utf-8"), method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read().decode("utf-8"))
        if result["code"] == 0 and result["data"]["signDays"] != 0:
            print("签到成功，本周已签到" + str(result["data"]["signDays"]) + "天")
        elif result["code"] == 0 and result["data"]["signDays"] == 0:
            print("今日已签到")
        else:
            print("签到失败")
    except Exception as e:
        print(f"签到异常: {e}")

def myRedBeanRecords():
    print("**开始查询豆子详情:**")
    datas = f"parActivityId={parActivityId}&wm_latitude={wm_latitude}&wm_longitude={wm_longitude}&token={token}&userPortraitId={portraitId}&pageNum=1"
    url = baseurl + "/cfeplay/playcenter/batchgrabred/myRedBeanRecords"
    req = urllib.request.Request(url, headers=head, data=datas.encode("utf-8"), method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read().decode("utf-8"))
        if result["code"] == 0:
            total = result["data"]["totalObtainAmount"]
            used = result["data"]["usedAmount"]
            expired = result["data"]["expiredAmount"]
            left = total - used - expired
            print(f"总获得: {total}, 已用: {used}, 过期: {expired}, 剩余: {left}")
        else:
            print("查询失败")
    except Exception as e:
        print(f"查询异常: {e}")

def exchange():
    print("**尝试兑换必中符:**")
    wm_actual_latitude = wm_latitude
    wm_actual_longitude = wm_longitude
    datas = f"wm_actual_longitude={wm_actual_longitude}&wm_actual_latitude={wm_actual_latitude}&exchangeRuleId=&propId={propId}&exchangeCoinNumber={exchangeCoinNumber}&parActivityId={parActivityId}&wm_ctype={wm_ctype}&wm_latitude={wm_latitude}&wm_longitude={wm_longitude}&token={token}"
    url = baseurl + "/cfeplay/playcenter/batchgrabred/exchange"
    req = urllib.request.Request(url, headers=head, data=datas.encode("utf-8"), method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read().decode("utf-8"))
        if result["code"] == 0:
            print("兑换成功")
        else:
            print("兑换失败: " + result.get("msg", ""))
    except Exception as e:
        print(f"兑换异常: {e}")

def querymyProps():
    print("**查询道具库:**")
    datas = f"parActivityId={parActivityId}&wm_latitude={wm_latitude}&wm_longitude={wm_longitude}&token={token}"
    url = baseurl + "/cfeplay/playcenter/batchgrabred/myProps"
    req = urllib.request.Request(url, headers=head, data=datas.encode("utf-8"), method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read().decode("utf-8"))
        if result["code"] == 0 and result["data"]:
            print(f"共有{len(result['data'])}个道具")
            for i, prop in enumerate(result['data']):
                if prop["status"] == 1:
                    print(f"有效道具{i+1}: {prop['propName']}, 过期时间: {prop['expireTime']}")
        else:
            print("道具库为空")
    except Exception as e:
        print(f"查询道具异常: {e}")

def getbatchId():
    print("**获取batchId:**")
    datas = f"parActivityId={parActivityId}&wm_ctype={wm_ctype}&wm_latitude={wm_latitude}&wm_longitude={wm_longitude}&token={token}"
    url = baseurl + "/cfeplay/playcenter/batchgrabred/corepage"
    req = urllib.request.Request(url, headers=head, data=datas.encode("utf-8"), method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read().decode("utf-8"))
        if result["code"] == 0 and "batchId" in result["data"]:
            return result["data"]["batchId"]
        else:
            print("获取batchId失败，可能非抢红包时间")
            return None
    except Exception as e:
        print(f"获取batchId异常: {e}")
        return None

def drawlottery(batchId):
    print("**抢红包:**")
    datas = f"parActivityId={parActivityId}&wm_latitude={wm_latitude}&wm_longitude={wm_longitude}&token={token}&batchId={batchId}&isShareLink=true&propType=1&propId=2"
    url = baseurl + "/cfeplay/playcenter/batchgrabred/drawlottery"
    req = urllib.request.Request(url, headers=head, data=datas.encode("utf-8"), method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read().decode("utf-8"))
        if result["code"] == 0:
            print("领取成功！红包价值: " + result["data"]["showTitle"])
        else:
            print("抢红包失败: " + result.get("msg", ""))
    except Exception as e:
        print(f"抢红包异常: {e}")

def pushPlus():
    if not webhook:
        print("webhook为空，不推送")
        return
    print("**开始推送企业微信:**")
    # 从收集器获取所有输出
    message = log_collector._buff if log_collector._buff else "无详细日志"
    # 限制长度，避免超出企业微信限制（最多2048字节）
    if len(message) > 2000:
        message = message[:2000] + "\n...（日志过长已截断）"
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(webhook, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read().decode("utf-8"))
        if result.get("errcode") == 0:
            print("企业微信推送成功")
        else:
            print("推送失败: " + json.dumps(result))
    except Exception as e:
        print(f"推送异常: {e}")

def main():
    print("脚本启动时间:", datetime.datetime.now())
    if not token:
        print("错误: token 为空，请检查环境变量")
        return
    signForBeans()
    doAction()
    myRedBeanRecords()
    # exchange()  # 可根据需要启用
    querymyProps()
    batchId = getbatchId()
    if batchId:
        drawlottery(batchId)
    if yesornot2 == "y":
        pushPlus()
    else:
        print("推送未开启")

if __name__ == "__main__":
    main()
