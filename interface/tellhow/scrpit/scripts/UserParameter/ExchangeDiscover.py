# -*- coding:utf-8 -*-
# 交换节点监控
import requests
import json
import sys
import time

def work(url):
    with requests.get(url) as req:
        resp = json.loads(req.text)
        json1 = resp["metrics"]
        #print json1
        for s in json1:
            #print s['values']
            i = s['values']
            for x in i:
                #print i[x]
                l = json.loads(i[x])
        for s in l:
            for x in s.keys():
                if type(s[x]) == type(u'unicode'):
                    #print "%s:%s" %(x,s[x])
                    print x,
                    print s[x].encode('utf8')
                else:
                    print "%s %s" % (x, s[x])
                #print type(s[x])
            print '------------------'

def nonredundant(url):
    with requests.get(url) as req:
        resp = json.loads(req.text)
        json1 = resp["metrics"]
        #print json1
        reinn = []
        for s in json1:
            #print s['values']
            i = s['values']
            for x in i:
                #print i[x]
                l = json.loads(i[x])
        for s in range(len(l)-1):
            if s == 1:
                #print l[s]['host']
                reinn += [{'{#SQL_NAME_COL}': str(l[s]['host'])}]
            if l[s]['host']!=l[s+1]['host']:
                #print l[s]['host']
                reinn += [{'{#SQL_NAME_COL}': str(l[s]['host'])}]
            #reinn += [{'{#SQL_NAME_COL}':str(l[s]['host'])}]
        result = {"data": reinn}
        # 避免转成json的时候 更换其编码
        rejson = json.dumps(result, ensure_ascii=False)
        print(rejson.encode('utf8'))

if __name__ == "__main__":
    curTime = time.time()
    #现在结束
    endTime = str(int(round(curTime)))
    #五分钟前开始
    #变成毫秒 乘 1000
    startTime = str(int(round((curTime-300))))
    #print type(startTime)
    #指定日期开始 2018-07-02 01:42:07
    #startTime = "1530466927"

    url = 'http://10.10.10.23/monitor/v1/timeline/metrics?metricNames=gxjhExchangeLog&hostName=192.168.0.10&appId=jinxin&startTime='+startTime+'&endTime='+endTime+'&precision=12'
    url1 = 'http://10.10.10.23/monitor/v1/timeline/metrics?metricNames=gxjhExchangeLog&hostName=192.168.0.10&appId=jinxin&startTime=1542188760&endTime=1542198760&precision=12'
    # execute = sys.argv[1]
    # if execute == 1:
    #     nonredundant(url)
    # elif execute == 2:
    #     work(url)
    work(url)
    #nonredundant(url)