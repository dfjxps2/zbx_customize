# -*- coding:utf-8 -*-
#阅读hdfs上日志的思路，经过观察hdfs上的日志生成有三种情况，一种是及时生成的，一种的一次生成一天的（也就是今天凌晨生成昨天的日志），yarn组件的日志是一直没有更新过的，
#我认为将当天（北京时间）的日志作为一个整体来看待，读的流程是先下载到本地 然后读本地的目录
from hdfs import *
import ConfigParser
import datetime
import os
import json
import time


#定义全局变量
#配置文件路径
log_read_conf = "D://pythonDev//Python2//AutoDiscovery//conf//readlog.conf"
#log_read_conf = "/etc/zabbix/scripts/config/readlog.conf"
#hdfs地址
hdfsHost = "http://s1:50070"

def hdfsLogRead():
    #get python-hdfs connection
    client = Client("http://s1:50070")
    #inital dir
    initalPath = "/ranger/audit"
    #get initlPath's instance
    dir1 = client.list(initalPath)
    # 获取当天日期 format 为 YYYYmmdd
    now_time = datetime.datetime.now().strftime('%Y%m%d')
    conf = logReadConf()
    # 获取配置文件option
    #option = conf.options()
    for s in range(len(dir1)):
        #拼接成组件目录 获得日期目录
        component = initalPath + "/" + str(dir1[s])
        componentPath = client.list(initalPath+"/"+dir1[s])
        #print(componentPath)
        #根据组件目录获取日期目录集
        #logFileDirList = client.list(componentPath)
        logFileDirList = componentPath
        #获取当前下载的日期目录名
        logDateDir = logFileDirList[len(logFileDirList)-1]
        #根据日期目录获取相应文件下的日式文件 我们现在只获取当前的前一天 所以要拼接目录名
        logFileName = client.list(component+"/"+logFileDirList[len(logFileDirList)-1])
        #print(logFileName)
        #获取文件名
        logName = logFileName[0]
        #拼接日志总路径
        logFilePath = component+"/"+logFileDirList[len(logFileDirList)-1]+"/"+ logName
        #昨天的日志总路径
        logFilePath1 = component+"/"+logFileDirList[len(logFileDirList)-2]+"/"+ logName
        #配置 配置文件中的文件名和当前下载日志文件的日期目录名 初始化数据
        #print conf.has_section(logName)
        #conf.add_section('aaaaa')
        if conf.has_section(logName) == False:
            conf.add_section(logName)
            conf.set(logName,logName,logDateDir)
            conf.set(logName,'linenumber',0)
            conf.set(logName,'logdate',now_time)
            conf.write(open(log_read_conf,'w'))
            #conf.write()
            client.download(logFilePath, "../logs/", overwrite=True)
        #获取当天的日期格式为YYYYmmdd
        dailyDate = now_time = datetime.datetime.now().strftime('%Y%m%d')
        #print(int(conf.get(logName,'logdate'))+3 < int(dailyDate))
        #if int(conf.get(logName,'logdate'))+3 < int(dailyDate):
        # print(int(conf.get(logName,'logdate')) == int(dailyDate))
        # print int(conf.get(logName,'logdate'))
        # print int(dailyDate)
        # 如果日期就是本天的 那么就每执行一次这个脚本就要重新下载一遍
        if int(conf.get(logName,'logdate')) == int(dailyDate):
            #下载日志文件
            client.download(logFilePath,"../logs/",overwrite=True)
            conf.set(logName,logName,logFileDirList[len(logFileDirList)-1])
            conf.set(logName, 'logdate', now_time)
            #如果下载的今天的日志是空的那么就下载昨天的日志
            if os.path.getsize("../logs/"+logName) == long(0):
                client.download(logFilePath1,"../logs/",overwrite=True)
                conf.set(logName, logName, logFileDirList[len(logFileDirList) - 2])
            conf.write(open(log_read_conf, 'w'))
        #如果日志是昨天的 那么防止有部分日志没有被读到 所以就再下载一次昨天的日志 然后触发读日志逻辑
        elif int(conf.get(logName,'logdate'))+1 == int(dailyDate):
            client.download(component+"/"+logFileDirList[len(logFileDirList)-2]+"/"+ logName,"../logs/",overwrite=True)
            conf.set(logName,'logdate',int(now_time)-1)
            conf.write(open(log_read_conf, 'w'))

def logReadConf():
    class myconf(ConfigParser.ConfigParser):
        def __init__(self, defaults=None):
            ConfigParser.ConfigParser.__init__(self, defaults=None)

        def optionxform(self, optionstr):
            return optionstr
    conf = myconf()
    #配置文件路径
    conf.read(log_read_conf)
    return conf

def confLog():
    import logging.handlers
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)
    # 日志格式
    formatter = logging.Formatter('[%(name)s]:[%(levelname)s]:[%(created)f]:[%(asctime)s]:[%(message)s]')
    # 日志执行者
    console = logging.StreamHandler()
    #console.setFormatter(formatter)
    fh = logging.handlers.SysLogHandler(('10.10.10.42', 6697), logging.handlers.SysLogHandler.LOG_AUTH)
    #fh.setFormatter(formatter)
    logger.addHandler(console)
    logger.addHandler(fh)
    return logger

def logFileRead():
    logger = confLog()
    #日志下载目录
    logDir = "../logs/"
    logFileList = []
    conf = logReadConf()
    # 获取当天的日期格式为YYYYmmdd
    dailyDate = datetime.datetime.now().strftime('%Y%m%d')
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
    for root,dirs,files in os.walk(logDir):
        logFileList = files
    #print logFileList
    for s in range(len(logFileList)):
        #如果读的是今天的日志那么就走按行读的逻辑
        if int(conf.get(logFileList[s],'logdate'))==int(dailyDate):
            with open("..//logs//"+logFileList[s],'r') as reader:
                contentList = reader.readlines()

                #获取上次读了多少行
                lastReadLine = conf.get(logFileList[s],'linenumber')
                # print(type(lastReadLine))
                #                 # print(type(len(contentList)))
                #从上次读的行开始读
                for i in range(int(lastReadLine),len(contentList)-1):
                    dict = eval(contentList[i])

                    # print type(dict)
                    #                     # print dict
                    # print("策略id: "+str(dict['repoType'])),
                    # print("事件时间: "+str(dict['evtTime'])),
                    # print("用户: "+str(dict['reqUser'])),
                    # print("服务名称/服务类型:"+str(dict['repo'])),
                    # #print("源名称/源类型: "+str(dict['resource'])),
                    # print("访问类型: "+str(dict['access'])),
                    # print("结果: "+str(dict['result'])),
                    # print("访问执行者: "+str(dict['enforcer'])),
                    # #print("客户端IP地址: "+str(dict['cliIP'])),
                    # print("事件数: "+str(dict['event_count']))
                    #logger.info("策略id啊: " + str(dict['repoType']) + " 事件时间: " + str(dict['evtTime']) + " 用户: " + str(dict['reqUser']) + " 服务名称或者服务类型:" + str(dict['repo'])  + " 访问类型: " + str(dict['access']) + " 结果: " + str(dict['result']) + " 访问执行者: " + str(dict['enforcer'])  + " 事件数: " + str(dict['event_count']))
                    #logger.info("[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]",str(dict['repoType']),str(dict['evtTime']),str(dict['reqUser']),str(dict['repo']),str(dict['resource']),str(dict['access']),str(dict['result']),str(dict['enforcer']),str(dict['cliIP']),str(dict['event_count']))
                    #print dict['evtTime']
                    #将毫秒级的时间格式转为秒级的时间格式
                    time_stamp = time.strptime(dict['evtTime'],'%Y-%m-%d %H:%M:%S.%f')
                    time_stamp = float(time.mktime(time_stamp))
                    event_time =time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time_stamp))

                    logger.info("[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]",str(dict['repoType']),event_time,str(dict['reqUser']),str(dict['repo']),'habase_master',str(dict['access']),str(dict['result']),str(dict['enforcer']),'o',str(dict['event_count']))

                    #logger.info("{}--->{}--->{}--->{}--->{}", "系统操作员ID", "被操作用户ID", "被操作ID类型", "操作时间", "操作描述");
                #将本次的行数记录下来 下次读
                conf.set(logFileList[s],'linenumber',len(contentList)-1)
                conf.write(open(log_read_conf, 'w'))
                #print 1
        #如果现在的日期是昨天的
        elif int(conf.get(logFileList[s],'logdate'))+1 == int(dailyDate):
            #接着昨天的行数读
            with open("..//logs//"+logFileList[s]) as reader:
                contentList = reader.readlines()
                #获取上次读了多少行
                lastReadLine = conf.get(logFileList[s],'linenumber')
                #从上次读的行开始读
                for i in range(int(lastReadLine),len(contentList)):
                    dict = eval(contentList[i])
                    logger.info("策略id: " + str(dict['repoType']) + " 事件时间: " + str(dict['evtTime']) + " 用户: " + str(dict['reqUser']) + " 服务名称/服务类型:" + str(dict['repo']) + " 访问类型: " + str(dict['access']) + " 结果: " + str(dict['result']) + " 访问执行者: " + str(dict['enforcer']) + " 事件数: " + str(dict['event_count']))
                #重置数据
                conf.set(logFileList[s],'linenumber',0)
                conf.set(logFileList[s],'logdate',dailyDate)
                conf.write(open(log_read_conf, 'w'))

if __name__ == "__main__":
    # print 1
    # now_time = datetime.datetime.now().strftime('%Y%m%d')
    # print now_time
    # print type(now_time)
    hdfsLogRead()
    logFileRead()
