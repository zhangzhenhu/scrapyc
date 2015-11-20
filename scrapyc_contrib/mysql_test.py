    # -*- coding: utf-8 -*-       
    #mysqldb      
    import time, MySQLdb      
         
    #连接      
    conn=MySQLdb.connect(host="localhost",user="wangpan",passwd="wangpan",db="wangpan",charset="utf8")    
    cursor = conn.cursor()      
      
    # #删除表  
    # sql = "drop table if exists user"  
    # cursor.execute(sql)  
      
    # #创建  
    # sql = "create table if not exists user(name varchar(128) primary key, created int(10))"  
    # cursor.execute(sql)  
      
    # #写入      
    # sql = "insert into user(name,created) values(%s,%s)"     
    # param = ("aaa",int(time.time()))      
    # n = cursor.execute(sql,param)      
    # print 'insert',n      
         
    # #写入多行      
    # sql = "insert into user(name,created) values(%s,%s)"     
    # param = (("bbb",int(time.time())), ("ccc",33), ("ddd",44) )  
    # n = cursor.executemany(sql,param)      
    # print 'insertmany',n      
      
    # #更新      
    # sql = "update user set name=%s where name='aaa'"     
    # param = ("zzz")      
    # n = cursor.execute(sql,param)      
    # print 'update',n      
         
    #查询      
    import pdb
    pdb.set_trace()
    n = cursor.execute("select * from baidu_user limit 10")      
    for row in cursor.fetchall():      
        print row  
        for r in row:      
            print r      
         
    # #删除      
    # sql = "delete from user where name=%s"     
    # param =("bbb")      
    # n = cursor.execute(sql,param)      
    # print 'delete',n      
      
    # #查询      
    # n = cursor.execute("select * from user")      
    # print cursor.fetchall()      
      
    cursor.close()      
         
    #提交      
    conn.commit()  
    #关闭      
    conn.close()     