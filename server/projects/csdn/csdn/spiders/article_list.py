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
import lxml.html
import lxml.etree


class UserSpider(scrapy.Spider):
    name = "article_list"
    allowed_domains = [ ]
    start_urls = []
    
    def __int__(self):
        scrapy.Spider.__init(self)

    def requestArticleList(self,user,pagenum=1):
        return scrapy.Request('http://blog.csdn.net/%s/article/list/%d'%(user,pagenum),callback=self.parseArticleList)


    def start_requests(self):
        M_SQLDB_CONF = self.settings.get("M_SQLDB_CONF")
        assert M_SQLDB_CONF, "Please set SQL DATABASE conf in baidu/settings.py ! eg:M_SQLDB_CONF={'host':'localhost','port':3306,'user':'wangpan','passwd':'wangpan','db':'wangpan'}"
        self._msql_config=M_SQLDB_CONF
        self._sql_connect()
        #self._sql_str="select uk from baidu_user;"
        self.user_list=['lmj623565791']     
        cursor = self.sql_conn.cursor()     
        cursor.execute("select username from user limit 0")
        for row in cursor.fetchall():
            self.user_list.append( row[0])
        self.sql_conn.commit()
                
        self.log("select total %d user message, **level"%len(self.user_list),level=log.INFO)
        for user in self.user_list:
                yield self.requestArticleList(user)


    def _sql_connect(self):
        self.sql_conn=MySQLdb.connect(**self._msql_config)

    def  parseArticleList(self,response):

        username=response.url.split("?")[0].split('/')[-1]

        self.log("GET article list succ. user:%s url:%s"%(username,response.url),level=scrapy.log.INFO)
        tree=lxml.html.fromstring(response.body.decode("utf-8"))
        #pdb.set_trace()
        for div_article in tree.xpath("//div[@id='article_list']/div"):
            article_url=div_article.xpath("div[@class='article_title']/h1//a/@href")[0]
            article_id = article_url.split("/")[-1]
            article_title=div_article.xpath("div[@class='article_title']/h1//a/text()")[0]
            #article_description=div_article.xpath("div[@class='article_description']/text()")[0]
            article_manage =div_article.xpath("div[@class='article_manage']")[0]
            link_postdate =article_manage.xpath("span[@class='link_postdate']/text()")[0].replace(" ","T")
            link_view = article_manage.xpath("span[@class='link_view']/text()")[0].replace("(","").replace(")","")
            link_comments=article_manage.xpath("span[@class='link_comments']/text()")[0].replace("(","").replace(")","")

            
            yield CsdnArticleItem(table_action="update",
                            username=username,
                            article_id=article_id,
                            article_url=article_url,
                            article_title=article_title,
                            #article_description=article_description,
                            postdate=link_postdate,
                            view=link_view,
                            comments=link_comments,
                            last_insert_time=str(datetime.datetime.now())
                            )
        for a in tree.xpath("//div[@id='papelist']/a"):
            if a.text_content() == u"下一页":
                yield scrapy.Request("http://blog.csdn.net"+a.get("href"),callback=self.parseArticleList)

    
    