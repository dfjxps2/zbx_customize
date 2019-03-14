# -*- coding:utf-8 -*-
import json
import pymysql
# import ConfigParser
#
# class myconf(ConfigParser.ConfigParser):
#     def __init__(self,defaults=None):
#         ConfigParser.ConfigParser.__init__(self,defaults=None)
#     def optionxform(self, optionstr):
#         return optionstr
# conf=myconf()
# conf.read("/etc/zabbix/scripts/config/db.conf")
# option= conf.sections()
# host = conf.get(option[0],'host')
# port = int(conf.get('db','port'))
# user = conf.get('db','user')
# db = conf.get('db','db')
# passwd = conf.get('db','passwd')
# charset = conf.get('db','charset')
host = '10.10.10.42'
port = 3306
user = 'root'
db = 'portaldb'
passwd = '123456'
charset = 'utf8'

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
sql='update sys_user set user_state=0 where user_id=17'
row_count = cursor.execute(sql)
row_3 = cursor.fetchall()
conn.commit()
cursor.close()
conn.close()
