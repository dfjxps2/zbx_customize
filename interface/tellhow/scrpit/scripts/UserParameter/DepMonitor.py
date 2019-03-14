# -*- coding:utf-8 -*-
import pymysql
import sys
import traceback
import ConfigParser



def user_monitor(username):
    try:
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
        # host = '10.1.3.193'
        # port = 3306
        # user = 'root'
        # db = 'portaldb'
        # passwd = 'root'
        # charset = 'utf8'
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        cursor = conn.cursor()
        #游标设置为字典类型
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    except Exception:
        print("接口请求数据失败")
        print('traceback.format_exc():\n%s' % traceback.format_exc())
        cursor.close()
        conn.close()
    else:
        usname = username
        sql = "select c.dep_id,d.dep_name,b.user_name,a.log_detail,SUM(a.user_op_type=0) as loginNum from user_access_log a,sys_user b,user_dep_rela c,user_department d where a.user_id=b.user_id and b.user_id =c.user_id and c.dep_id = d.dep_id"
        sql+=" and d.super_dep_id = (select dep_id from user_department where dep_name = '{0}')".format(usname)
        #系统当天零点时间
        sql+=" and a.log_time >= (SELECT DATE_FORMAT(CURDATE(),'%Y-%m-%d %H:%i:%s'))"
        row_count = cursor.execute(sql)
        row_3 = cursor.fetchall()
        #print(row_3)
        if row_3[0]["loginNum"]==None :
            print(0)
        else :
            for i in row_3:
                print(i["loginNum"])

        # for i in range(len(row_3)):
        #     print(row_3)

        conn.commit()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    user_monitor(sys.argv[1])
    #user_monitor('市经济信息化委')