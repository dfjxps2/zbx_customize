# coding: utf-8
import sys
import json
import requests
import traceback
import re
def mea_query(url,sys_name,datatype):
    try:
        rs = requests.get(url)
        content = rs.text
        body = json.loads(content)
        l = body["metrics"]
    except Exception:
        print("接口请求数据失败")
        print('traceback.format_exc():\n%s' % traceback.format_exc())
    else:
        # 遍历列表
        for i in l:
            # print(i["values"])
            s = i["values"]
            #print s
            #print type(s)
            for x in s:
                #print s[x]
                json2 = json.loads(s[x])
                #print json2
                #print json2[0]
        for s in json2:
            #print s['serviceName'].encode('utf8')
            #print(re.match('(.*)深网爬虫模块(.*)',s['serviceName'].encode('utf8')))
            #根据传来的系统名 然后 用正则 去匹配去哪条数据
            if re.match('(.*)'+sys_name+'(.*)',s['serviceName'].encode('utf8'))!= None:
                if datatype == 'calltime':
                    print(s['serviceCallTime'])
                elif datatype == 'dataLength':
                    print(s['serviceDataLength'])
                # print(s['serviceName']),
                # print(s['serviceDataLength']),
                # print(s['serviceCallTime'])
            #if re.match('深网爬虫模块',s['serviceName'].encode('utf8')):
        #     for key, value in s.items():
        #         #print(value.encode('utf8'))
        #         json2 = value
        #         print json2
        #         print json2[0]
        # print json2[0]
def args(args):
    print args[1]
    print args[2]
    print args[3]
if __name__ == "__main__":
    #sys_name = sys.argv
    #args(sys.argv)
    ip = sys.argv[1]
    sys_name = sys.argv[2]
    datatype = sys.argv[3]
    #sys_name = '深网爬虫模块'
    #mea_query("http://10.10.10.35:7788/smcs-api/monitor/v1/timeline/metrics?metricNames=state&appId=YARN/NodeManager")
    mea_query("http://10.10.10.23/monitor/v1/timeline/metrics?metricNames=serviceCalllog&hostName=a&appId=b&startTime=1541651940&endTime=1541652000&precision=10",sys_name,datatype)