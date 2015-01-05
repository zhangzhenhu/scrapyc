import scrapy
import datetime
import time
#from alibaba import settings
import re
#from twisted.enterprise import adbapi
#import MySQLdb.cursors
import urlparse
import json
from scrapy import log
from alibaba.items import ShopItem,GoodsItem,IndexItem
#from scrapy.conf import settings
from scrapy.utils.url import parse_url

class ShopSpider(scrapy.Spider):
    name = "shop"
    allowed_domains = [ ]
    start_urls = []
    
    def __init__(self,*args, **kwargs):
        super(ShopSpider, self).__init__(*args, **kwargs)
        self._kwargs = kwargs




    
    def start_requests(self):

        
        # M_SQLDB_CONF = self.settings.get("M_SQLDB_CONF")
        # assert M_SQLDB_CONF, "Please set SQL DATABASE conf in alibaba/settings.py ! eg:M_SQLDB_CONF={'host':'localhost','port':3306,'user':'wangpan','passwd':'wangpan','db':'wangpan'}"
        
        # self._msql_config=M_SQLDB_CONF
        # self._sql_connect()

        requests = []
        requests.append(scrapy.Request('http://jinpai.1688.com/',callback=self.parse_jinpai))
                
        

        return requests

    def _sql_connect(self):
        self.sql_conn=MySQLdb.connect(**self._msql_config)

    def parse_jinpai(self, response):
        #response.status != 200
        self.log('[parse_jinpai] %d %s'%(response.status,response.url),level=scrapy.log.INFO)
        div = response.xpath('//*[@id="box_doc"]/div[1]/div/div[1]')
        for href in div.xpath("//a/@href").extract():
            if not href.startswith("http://"):
                continue
            scheme, netloc, path, params, query, fragment = parse_url(href)

            if netloc.startswith("shop") or path.endswith("creditdetail.htm"):

                yield ShopItem(url="%s://%s/"%(scheme,netloc),insert_time=str(datetime.datetime.now()))
            elif netloc == "detail.1688.com":
                yield GoodsItem(url=href,insert_time=str(datetime.datetime.now()))
            elif netloc == "go.1688.com":
                yield IndexItem(url=href,insert_time=str(datetime.datetime.now()))

            else:
                print href

        pass


