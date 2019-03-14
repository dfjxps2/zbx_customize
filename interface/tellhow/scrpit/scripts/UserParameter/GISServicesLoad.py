# coding: utf-8
# GIS ServicesLoad
import requests
import json
import sys

def request(url):
    with requests.get(url) as req:
        rep = json.loads(req.text)
        #print rep
        m = 0;
        for s in rep['historicalAccessCounts']:
            m +=s
        print m


if __name__ == "__main__":
    ip = sys.argv[1]
    #ip = "10.10.10.43:8091"
    #iServer需要token才能使用它的api
    token = sys.argv[2]
    #token  = "aWRkTmej9xYa5ft48SxMA7KAInXOcMWFbPt-Yrr4eBmB6NKvetOLeLhnEb8xfE0W_jefxTvvfzTurNLkk3ciTw."
    #url = "http://10.10.10.43:8091/iserver/manager/serverstatus/servicesload.json?token=aWRkTmej9xYa5ft48SxMA7KAInXOcMWFbPt-Yrr4eBmB6NKvetOLeLhnEb8xfE0W_jefxTvvfzTurNLkk3ciTw.."
    url = "http://"+ip+"/iserver/manager/serverstatus/servicesload.json?token="+token
    request(url)