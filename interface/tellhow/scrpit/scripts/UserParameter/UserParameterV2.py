# -*- coding:utf-8 -*-
import sys
import json
import requests
import traceback
import time
import argparse

def url_joint(metName,ipport):
    curTime = time.time()
    #现在结束
    endTime = str(int(round(curTime * 1000)))
    #五分钟前开始
    startTime = str(int(round((curTime-300) * 1000)))
    url = "http://"+ipport+"/monitor/v1/timeline/metrics?metricNames="+metName+"&hostName=a&appId=b&startTime="+startTime+"&endTime="+endTime+"&precision=10"
    #print(url)
    mea_query(url)

def mea_query(url):
    try:
        rs = requests.get(url)
        content = rs.text
        body = json.loads(content)
        #print body
        if body['status']!=0:
            print("接口请求失败，请查看接口状态")
            return
        else:
            l = body["metrics"]
    except Exception:
        print("接口请求数据失败")
        print('traceback.format_exc():\n%s' % traceback.format_exc())
    else:
        # 遍历列表
        for i in l:
            # print(i["values"])
            s = i["values"]
            for key, value in s.items():
                if value==None :
                    print(0)
                else:
                    print(value.encode('utf8'))

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--url',type = str ,default='tom')
    parser.add_argument('--metname',type=str,default='null')
    parser.add_argument('--ipport',type=str,default='null')
    return parser.parse_args(argv)

def main(args):
    # print(args.metname)
    # print(args.ipport)
    # print(args.url)
    if args.metname != 'null':
        #print(args.metname,args.ipport)
        url_joint(args.metname,args.ipport)
    elif (args.metname=='null'and args.ipport=='null')and args.url!='tom':
        #print(args.url)
        mea_query(args.url)

if __name__ == "__main__":
    main(parse_arguments(sys.argv[1:]))
    # one = ""
    # metName = "countTaskNumByTimes"
    # ipport = "10.10.10.23"
    # if metName == "countTaskNumByTimes":
    #     url_joint(metName,ipport)
    # else:
    #     mea_query(one)
    #mea_query("http://localhost:8081/monitor/v1/timeline?metricNames=time&hostName=agent1&appId=1")