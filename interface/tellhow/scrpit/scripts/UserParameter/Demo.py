
# coding: utf-8
import sys
import json
import requests

url = 'http://10.10.10.23/monitor/v1/timeline/metrics?metricNames=catalog&hostName=a&appId=b&startTime=100&endTime=200&precision=10'


rs = requests.get(url)
content = rs.text
body = json.loads(content)
l = body["metrics"]

# 遍历列表
for i in l:
    # print(i["values"])
    s = i["values"]
    for key, value in s.items():
        if value==None :
            print(0)
        else:
            print(value)



