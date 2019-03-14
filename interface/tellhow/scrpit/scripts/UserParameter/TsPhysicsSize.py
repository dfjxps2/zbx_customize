# coding: utf-8
import cx_Oracle
#'bsc_emp_lh/bsc_emp_lh@10.10.10.37/orcl'
# 'ZABBIX/ZABBIX@10.1.3.180/orcl'
db = cx_Oracle.connect('bsc_emp_lh/bsc_emp_lh@10.10.10.37/orcl11')
cr = db.cursor()
sql="SELECT tablespace_name, file_id, file_name, round(bytes / (1024 * 1024), 0) total_space FROM dba_data_files ORDER BY tablespace_name"
cr.execute(sql)
rs=cr.fetchall()
#print rs
# for i in rs:
# #    print i
#     for s in range(len(i)):
#         print("TableSpace_Name:"+i[0]+"File_Id:"),
#         print(i[1]),
#         print("File_Name"+i[2]+"Total_Space"),
#         print(i[3])
for i in rs:
    print("TableSpace_Name:"+i[0]+"File_Id:"),
    print(i[1]),
    print("File_Name"+i[2]+"Total_Space"),
    print(i[3])
#print(rs)
db.close()


