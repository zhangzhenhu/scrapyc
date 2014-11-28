import MySQLdb.cursors

M_SQLDB_CONF={"host":"localhost","port":3306,"user":"root","passwd":"root","db":"csdn","charset":'utf8'}
sql_conn=MySQLdb.connect(**M_SQLDB_CONF)
cursor = sql_conn.cursor()     
#cursor.execute("select username from user limit 0")

f=open("csdn_user.txt","r")
for row in f.readlines():
    row=row.strip().decode("gbk")
    cursor.execute('insert into user (username )values("%s")  ON DUPLICATE KEY UPDATE username ="%s";'%(row,row))
sql_conn.commit()
f.close()