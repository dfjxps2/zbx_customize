# -*- coding:utf-8 -*-
import json
import pymysql
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import ConfigParser

class myconf(ConfigParser.ConfigParser):
    def __init__(self,defaults=None):
        ConfigParser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        return optionstr
conf=myconf()
conf.read("/etc/zabbix/scripts/config/db.conf")
option= conf.sections()
host = conf.get(option[0],'host')
port = int(conf.get('db','port'))
user = conf.get('db','user')
db = conf.get('db','db')
passwd = conf.get('db','passwd')
charset = conf.get('db','charset')
# host = '10.10.10.42'
# port = 3306
# user = 'root'
# db = 'portaldb'
# passwd = '123456'
# charset = 'utf8'

# host = '127.0.0.1'
# port = 3306
# user = 'root'
# db = 'portaldb'
# passwd = 'root'
# charset = 'utf8'

conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db,charset=charset)
cursor = conn.cursor()
number = 3
#游标设置为字典类型
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
row_count = cursor.execute("SELECT a.dep_name as colname"
	+" from user_department a"
	+" WHERE a.super_dep_id is NULL"
	+" and a.dep_state = 1")
row_3 = cursor.fetchall()
# for s in row_3:
# 	print(s['colname'].encode("utf-8"))

reinn= []
for i in row_3:
    # reinn={"{#SQL_NAME_COL}",i["username"]}
    reinn += [{'{#SQL_NAME_COL}':i["colname"]}]

result = {"data":reinn}
#避免转成json的时候 更换其编码
rejson = json.dumps(result,ensure_ascii=False)
print(rejson.encode('utf8'))

conn.commit()
cursor.close()
conn.close()
