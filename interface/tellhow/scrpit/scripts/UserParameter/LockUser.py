# -*- coding:utf-8 -*-
import pymysql


# import ConfigParser
#
# class myconf(ConfigParser.ConfigParser):
#     def __init__(self, defaults=None):
#         ConfigParser.ConfigParser.__init__(self, defaults=None)
#
#     def optionxform(self, optionstr):
#         return optionstr
#
#
# conf = myconf()
# conf.read("/etc/zabbix/scripts/config/db.conf")
# option = conf.sections()
# host = conf.get(option[0], 'host')
# port = int(conf.get('db', 'port'))
# user = conf.get('db', 'user')
# db = conf.get('db', 'db')
# passwd = conf.get('db', 'passwd')
# charset = conf.get('db', 'charset')
host = '10.10.10.42'
port = 3306
user = 'root'
db = 'portaldb'
passwd = '123456'
charset = 'utf8'
conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
cursor = conn.cursor()
number = 3
#游标设置为字典类型
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
# 执行参数化查询
#when '0' then'登录' when '1'then '退出' when '2'then '调用菜单'
sql = "select s.user_id from (select b.user_id ,SUM(c.user_op_type=0) as loginNum from user_role a  LEFT JOIN user_role_rela b on a.role_id = b.role_id	LEFT JOIN user_access_log c on b.user_id = c.user_id where a.role_name <> '系统管理员' and c.log_time >= (SELECT DATE_FORMAT(CURDATE(),'%Y-%m-%d %H:%i:%s'))) s where loginNum > 100 "
#sql1='select user_id from sys_user where job_id = 4'
cursor.execute(sql)
row_3 = cursor.fetchall()
if len(row_3)!=0:
    b = []
    for i in range(len(row_3)):
        b.append(row_3[i]['user_id'])
    # print(tuple(b))
    num = tuple(b)
    sql2 = 'UPDATE sys_user x SET x.user_state = 0 WHERE x.user_id in {0}'.format(num)
    #print(sql2)
    effect = cursor.execute(sql2)

conn.commit()
cursor.close()
conn.close()