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
host = conf.get(option[0], 'host')
port = int(conf.get('db', 'port'))
user = conf.get('db', 'user')
db = conf.get('db', 'db')
passwd = conf.get('db', 'passwd')
charset = conf.get('db', 'charset')

#host = '10.1.3.193'
#port = 3306
#user = 'root'
#db = 'portaldb'
#passwd = 'root'
#charset = 'utf8'
conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
cursor = conn.cursor()
number = 3
#游标设置为字典类型
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
# 执行参数化查询
# when '0' then'登录' when '1'then '退出' when '2'then '调用菜单'
sql = "select a.log_time,a.user_ip,a.log_detail from user_access_log a"
sql+= " where a.log_time >= (select CURRENT_TIMESTAMP - INTERVAL 10 MINUTE)"
row_count = cursor.execute(sql)
row_3 = cursor.fetchall()

#print(row_3)
if row_count == 0:
    print("用户无操作")
else:
    for i in row_3:
        print(i['log_detail'].encode('utf8'))


# for i in range(len(row_3)):
#     print(row_3)

conn.commit()
cursor.close()
conn.close()
