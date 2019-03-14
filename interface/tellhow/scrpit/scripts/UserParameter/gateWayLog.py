import requests
import json
import logging.handlers
import time

def work(url):
    with requests.get(url) as req:
        jresp = json.loads(req.text)
        body = jresp["metrics"]
        #print body
        logger=confLog()
        for i in body:
            #print i
            for s in i['values']:
                resp = json.loads(i['values'][s])
                #print resp
                for l in resp:
                    #print l
                    #print l['id']
                    #for k,v in l.items():
                    #print type(l['beginTime'])
                    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(l['beginTime']/1000))
                    #print start_time
                    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(l['endTime']/1000))
                    #logger.info("[%s]:[%s]",l['result'],l['resultExplain'])
                    result_explain = json.loads(l['resultExplain'])
                    #print result_explain['message']
                    logger.info("[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]",str(l['id']),l['ip'],l['url'],l['serviceName'],l['serviceName'],start_time,end_time,l['duringTime'],l['result'],result_explain['message'])
                    #logger.info(l['id'])
                    #logger.info("[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]", l['id'],l['ip'],l['url'],l['serviceName'],l['serviceName'],l['beginTime'],l['endTime'],l['duringTime'],l['result'],l['resultExplain']['message'])
                    #for k in l.keys():
                        #print("%s : %s"%(k,v))
                        #logger.info("[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]",[])
                    #print("--------------")



def confLog():
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    fh = logging.handlers.SysLogHandler(('10.10.10.42', 6698), logging.handlers.SysLogHandler.LOG_AUTH)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #fh.setFormatter(formatter)
    logger.addHandler(fh)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    #console.setFormatter(formatter)
    logger.addHandler(console)
    return logger

if __name__ == '__main__':
    stime = str(int(time.time()))
    etime = str(int(time.time())-300)
    url = 'http://10.10.10.23/monitor/v1/timeline/metrics?metricNames=gateWayLog&hostName=a&appId=jinxin&startTime='+stime+'&endTime='+etime+'&precision=2'
    work(url)

