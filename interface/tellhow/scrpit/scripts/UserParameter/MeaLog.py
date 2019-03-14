#coding: utf-8
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
index = option[0]
host = conf.get(index, 'host')
port = int(conf.get(index, 'port'))
user = conf.get(index, 'user')
db = conf.get(index, 'db')
passwd = conf.get(index, 'passwd')
charset = conf.get(index, 'charset')

#host = 'localhost'
#port = 3306
#user = 'root'
#db = 'portaldb'
#passwd = 'root'
#charset = 'utf8'
conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db,charset=charset)
cursor = conn.cursor()
#将游标设置为字典类型
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
sql="select * from ( select a.log_time,a.user_ip,a.log_detail from user_access_log a where a.log_time >= (select CURRENT_TIMESTAMP - INTERVAL 10 MINUTE)) b where INSTR(b.log_detail,'指标接口')"
#sql = "select a.log_time,a.user_ip,a.log_detail from user_access_log a where log_detail like '%指标接口%'"
cursor.execute(sql)
row_3 = cursor.fetchall()
for s in row_3:
    print s['log_detail'].encode('utf8')


conn.commit()
cursor.close()
conn.close()
