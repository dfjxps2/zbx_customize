# coding: utf-8
import cx_Oracle

db=cx_Oracle.connect('bsc_emp_lh/bsc_emp_lh@10.10.10.37/orcl11')
cr=db.cursor()
sql='SELECT t.tablespace_name, round(SUM(bytes / (1024 * 1024)), 0) ts_size FROM dba_tablespaces t, dba_data_files d WHERE t.tablespace_name = d.tablespace_name GROUP BY t.tablespace_name'
cr.execute(sql)
rs=cr.fetchall()
#print rs
for i in rs:
#    print i
#    for s in range(len(i)):
    print("TableSpace_Name:"+i[0]+"Ts:"),
    print(i[1])
#print(rs)
db.close()


