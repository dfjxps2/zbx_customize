# coding: utf-8
import sys
import json
import requests
import traceback

def mea_query(url):
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
            for key, value in s.items():
                print(value)

if __name__ == "__main__":
    mea_query(sys.argv[1])