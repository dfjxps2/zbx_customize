# -*- coding:utf-8 -*-
import json

#错误级别：0正常 1警告 2错误 3严重错误 9异常
num = [0,1,2,3,9]
num1 = ['正常','警告','错误','严重错误','异常']
#print(num1[0])
str = []
for i in range(len(num1)):
    str += [{'{#SQL_NAME_COL}':num1[i]}]

#print(str)

result = {"data":str}
#避免转成json的时候 更换其编码
rejson = json.dumps(result,ensure_ascii=False)
print(rejson)