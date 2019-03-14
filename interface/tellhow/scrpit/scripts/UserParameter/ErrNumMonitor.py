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
        index = option[1]
        host = conf.get(index, 'host')
        port = int(conf.get(index, 'port'))
        user = conf.get(index, 'user')
        db = conf.get(index, 'db')
        passwd = conf.get(index, 'passwd')
        charset = conf.get(index, 'charset')
        # host = '192.168.1.136'
        # port = 3306
        # user = 'root'
        # db = 'dg_dqc'
        # passwd = 'root'
        # charset = 'utf8'
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        cursor = conn.cursor()
        #返回结果为字典类型
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    except Exception:
        print("")
        print('traceback.format_exc():\n%s' % traceback.format_exc())
        cursor.close()
        conn.close()
    else:
        if username == '正常':
            username = 0
        elif username == '警告':
            username = 1
        elif username == '错误':
            username = 2
        elif username == '严重错误':
            username = 3
        elif username == '异常':
            username = 9
        else:
            print(0)
            return

        #sql = "SELECT A2.Task_Name,A1.Error_Level_Cd,A1.Tx_Date,A1.TaskRunTime,A2.DQID FROM M07_CHECKRESULT A1 INNER JOIN M07_CHECKLIST A2 ON A1.DQID = A2.DQID WHERE A1.Error_Level_Cd in (1,2,3,9) AND A2.Start_Dt <= A1.TaskRunTime  AND A2.End_Dt > A1.TaskRunTime "
        sql = "select a1.error_level_cd ,count(*) from m07_checkresult a1 inner join m07_checklist a2  on a1.dqid = a2.dqid where a1.error_level_cd in (1,2,3,9) and a2.start_dt <= a1.taskruntime  and a2.end_dt > a1.taskruntime"
        #系统前一天的时间
        #sql+="  and a1.tx_date = (select date_sub(curdate(),interval 1 day))"
        #要查询的异常级别
        sql +=" and a1.error_level_cd = '{0}'".format(username)
        sql +=" group by a1.error_level_cd"
        row_count = cursor.execute(sql)
        row_3 = cursor.fetchall()

#        print(row_3)
        if row_count==0:
            print(0)
        else:
            for i in row_3:
                print (i['error_level_cd'])


        conn.commit()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    user_monitor(sys.argv[1])
    #user_monitor('错误')