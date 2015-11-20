# -*- coding: utf-8 -*-
import scrapy
import datetime
import time
import re
from twisted.enterprise import adbapi
import MySQLdb.cursors
import urlparse
import json
from scrapy import log
from csdn.items import *
import csdn

class UserSpider(scrapy.Spider):
    name = "user"
    allowed_domains = [ ]
    start_urls = []
    
    def __int__(self):
        scrapy.Spider.__init(self)




    def requestUserList(self,user):
        return scrapy.Request('http://my.csdn.net/service/main/guess_like_experts?num=20&username=%s'%(user),callback=self.parseUserList)

    
    def start_requests(self):
        M_SQLDB_CONF = self.settings.get("M_SQLDB_CONF")
        assert M_SQLDB_CONF, "Please set SQL DATABASE conf in baidu/settings.py ! eg:M_SQLDB_CONF={'host':'localhost','port':3306,'user':'wangpan','passwd':'wangpan','db':'wangpan'}"
        self._msql_config=M_SQLDB_CONF
        self._sql_connect()
        #self._sql_str="select uk from baidu_user;"
        self.user_list=[]     
        cursor = self.sql_conn.cursor()     
        cursor.execute("select username from user")
        for row in cursor.fetchall():
            self.user_list.append( row[0])
        self.sql_conn.commit()
                
        self.log("select total %d user message, **level"%len(self.user_list),level=log.INFO)
        for user in self.user_list:
                yield self.requestUserList(user)


    def _sql_connect(self):
        self.sql_conn=MySQLdb.connect(**self._msql_config)


 

    def  parseUserList(self,response):
        jp=json.loads(response.body)
        if jp['err'] != 0 :
            self.log("GET baidu user fanlist error! errno:%d msg:%s url:%s"%(jp['err'],jp['msg'],response.url),level=scrapy.log.WARNING)
            return
        
        #print jp
        o = urlparse.urlparse(response.url)
        param_dict = urlparse.parse_qs(o.query)
        username=param_dict['username'][0]

        self.log("GET baidu user list succ. user:%s url:%s"%(username,response.url),level=scrapy.log.INFO)
        for userinfo in jp['result']:
            
            yield CsdnUserItem(table_action="update",
                            username=userinfo["username"],    
                            avatar_url=userinfo["avatar"],
                            last_insert_time=str(datetime.datetime.now())
                            )
            yield self.requestUserList(userinfo["username"])

    
    