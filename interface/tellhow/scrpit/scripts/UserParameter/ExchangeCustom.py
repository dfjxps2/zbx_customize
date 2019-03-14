# -*- coding:utf-8 -*-
# 交换节点监控
import requests
import json
import time
import sys
#取业务数据
def work(url,ip,column):
    with requests.get(url) as req:
        resp = json.loads(req.text)
        json1 = resp["metrics"]
        #print json1
        for s in json1:
            #print s['values']
            i = s['values']
            for x in i:
                #print i[x]
                #l为接口数据
                l = json.loads(i[x])
        #有意义的数据为 taskId相同且id为最大的这条数据
        #先获取本次数据所有的taskId
        key_list = []
        for s in l:
            key_list.append(s['taskId'])
        key_list = list(set(key_list))


        #获取taskId相同且 id最大的那条数据
        id_list = []
        sum_success = 0
        for s in key_list:
            for x in range(len(l)):
                if s == l[x]['taskId']:
                    #print ('x='+'%s'% l[x]['id'])
                    id_list.append(x)
            #print id_list[len(id_list)-1]
            #print l[id_list[len(id_list)-1]]
            #print l[id_list[len(id_list)-1]]['producer'].encode('utf8')
            #print l[id_list[len(id_list)-1]]['consumer'].encode('utf8')
            #print l[id_list[len(id_list) - 1]]['successCount']
            if l[id_list[len(id_list)-1]]['producer'].encode('utf8') == '中心节点':
                #print l[id_list[len(id_list)-1]]['successCount']
                #print l[id_list[len(id_list)-1]]['successCount']
                sum_success+=l[id_list[len(id_list)-1]]['successCount']
        #print("success:"+'%o'% sum_success)
        print sum_success


#发现节点ip
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
        #由于返回的数据会有很多重复的host，这里既然要以host来区分交换节点，那么就需要将host去重，也就是获取真正的交换节点到底有几个
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
    url2 = 'http://10.10.10.23/monitor/v1/timeline/metrics?metricNames=gxjhExchangeLog&hostName=192.168.0.10&appId=jinxin&startTime=1542188760&endTime=1542198760&precision=12'
    execute = sys.argv[1]
    if execute == '1':
        nonredundant(url2)
    elif execute == '2':
        ip = sys.argv[2]
        #if sys.argv[2] == None:
        #    ip = '192.168.1.106'
        column = 'successCount'
        work(url2,ip,column)
        #nonredundant(url2)
