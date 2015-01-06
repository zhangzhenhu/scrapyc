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
import urlparse
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
        if response.status != 200 :
            yield response.request 
            return

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
                yield Scrapy.Request(href,callback=self.parse_cateory)
            else:
                print href

        pass

    def parse_cateory(self,response):
        self.log('[parse_cateory] %d %s'%(response.status,response.url),level=scrapy.log.INFO)

        if response.status != 200 :
            yield response.request 
            return   
        for href in response.xpath('//*[@id="listbody"]/div[@class="supplier-list"]/div[@class="supplier"]/div[@class="title p-margin"]//a/@href').extract():
            if not href.startswith("http://"):
                continue 
            scheme, netloc, path, params, query, fragment = parse_url(href)
            yield ShopItem(url="%s://%s/"%(scheme,netloc),insert_time=str(datetime.datetime.now()))
        scheme, netloc, path, params, query, fragment = parse_url(response.url)
        qs = urlparse.parse_qs(query)
        pageStart = int(qs.get('pageStart',1))
        pageCount = int(qs.get('pageCount',0))
        if not pageCount:
            pageCount = response.xpath('//*[@id="pageCount"]/@value').extract()
            if len(pageCount) > 0:
                try:
                    pageCount = int(pageCount[0])
                except Exception, e:
                    pageCount = 1000

        if pageStart < pageCount:
            qs['pageStart'] = str(pageStart)
            qs['pageCount'] = str(pageCount)

            query = ""
            for k,v in qs.items():
                query += "&%s=%s"%(k,v)
            if query:
                query = query[1:]

            yield Scrapy.Request(urlparse.urlunparse( scheme, netloc, path, params,query),callback=self.parse_cateory)     
