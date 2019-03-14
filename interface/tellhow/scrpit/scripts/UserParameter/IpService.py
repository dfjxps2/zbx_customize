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
        # host = '10.10.10.42'
        # port = 3306
        # user = 'root'
        # db = 'portaldb'
        # passwd = '123456'
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
        sql = "select e.menu_cn_name as loginNum from user_dep_rela b left join user_role_rela c on b.user_id = c.user_id left join menu_privilege d on c.role_id = d.role_id left join sys_menu e on d.menu_id = e.menu_id left join sys_user f on b.user_id = f.user_id left join user_access_log g on g.user_id = f.user_id where e.super_menu_id not in(1,2,16,52,45,154) and e.menu_state = 1 and g.user_ip = '{0}' group by e.menu_cn_name".format(username)
        row_count = cursor.execute(sql)
        row_3 = cursor.fetchall()
        #print(row_3)
        if row_3 == () :
            print('当前无订阅')
        else :
            for i in row_3:
                print(i["loginNum"].encode('utf8'))

        # for i in range(len(row_3)):
        #     print(row_3)

        conn.commit()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    user_monitor(sys.argv[1])
    #user_monitor("10.1.0.221")