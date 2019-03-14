# -*- coding:utf-8 -*-
import pymysql
import ConfigParser

class myconf(ConfigParser.ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=None)
    def optionxform(self, optionstr):
        return optionstr


conf = myconf()
conf.read("/etc/zabbix/scripts/config/db.conf")
option = conf.sections()
index = option[2]
host = conf.get(index, 'host')
port = int(conf.get(index, 'port'))
user = conf.get(index, 'user')
db = conf.get(index, 'db')
passwd = conf.get(index, 'passwd')
charset = conf.get(index, 'charset')

#host = 'localhost'
#port = 3306
#user = 'root'
#db = 'etldb'
#passwd = 'root'
#charset = 'utf8'
conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db,charset=charset)
cursor = conn.cursor()
#将游标设置为字典类型
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
sql="select Last_JobStatus  from etl_job where Last_EndTime > (select DATE_SUB(NOW(), INTERVAL 5 MINUTE)) "
cursor.execute(sql)
row_3 = cursor.fetchall()
#print(row_3)
result = 0
for s in row_3:
    if 'Failed'==s['Last_JobStatus']:
        result = 6
print result
conn.commit()
cursor.close()
conn.close()

