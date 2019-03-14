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
index = option[1]
host = conf.get(index, 'host')
port = int(conf.get(index, 'port'))
user = conf.get(index, 'user')
db = conf.get(index, 'db')
passwd = conf.get(index, 'passwd')
charset = conf.get(index, 'charset')
# host = '192.168.1.136'
# #host = 'localhost'
# port = 3306
# user = 'root'
# db = 'dg_dqc'
# passwd = 'root'
# charset = 'utf8'
conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db,charset=charset)
cursor = conn.cursor()
#将游标设置为字典类型
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
sql = "select a2.task_name,a1.error_level_cd,a1.tx_date,a1.taskruntime,a2.dqid from m07_checkresult a1 inner join m07_checklist a2 on a1.dqid = a2.dqid where a1.error_level_cd in (1,2,3,9)  "
sql += "and a2.start_dt <= a1.taskruntime  and a2.end_dt > a1.taskruntime"
#sql += " AND A1.tx_date = (select date_sub(curdate(),interval 1 day))"
cursor.execute(sql)
row_3 = cursor.fetchall()
#print(row_3)
for i in row_3:
    #print i
    #print i.keys()
    for s in i.keys():
        #print "%s:%s" % (i,i[s])
        if s=='task_name':
            print '|',
            print s,
            print ':',
            print i[s].encode('utf8'),
        else:
            print '|',
            print s,
            print ':',
            print i[s],
        #print(i[s].encode('utf8'))
    print ' '

conn.commit()
cursor.close()
conn.close()

