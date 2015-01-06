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


def parse_query(query):
    if not query:
        return {}
    ret = {}
    for item in query.split("&"):
        item = item.strip()
        if not item:
            continue
        item = item.split('=',1)
        if len(item) == 2:
            ret[item[0]] =item[1]
        else:
            ret[item[0]] = None
    return ret



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
        requests.append(scrapy.Request('http://go.1688.com/supplier/gold_supplier.htm',callback=self.parse_index))
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
            elif netloc == "go.1688.com" and 'supplier' in path:
                yield IndexItem(url=href,insert_time=str(datetime.datetime.now()))
                yield scrapy.Request(href,callback=self.parse_index)


        pass

    def parse_index(self,response):
        self.log('[parse_index] %d %s'%(response.status,response.url),level=scrapy.log.INFO)

        if response.status != 200 :
            yield response.request 
            return   
        #parse category
        for href in response.xpath('//*[@id="hotwordpanel"]//li/@data-url').extract()+response.xpath('//*[@id="hotwordpanel"]//a/@href').extract():
            if not href.startswith("http://"):
                continue 
            scheme, netloc, path, params, query, fragment = parse_url(href)
            if netloc.startswith("shop") or path.endswith("creditdetail.htm"):
                shop_url = "%s://%s/"%(scheme,netloc)
                yield ShopItem(url=shop_url,insert_time=str(datetime.datetime.now()))
                self.log('[parse_index] found shop %s'%(shop_url),level=scrapy.log.INFO)
            elif netloc == "detail.1688.com":
                yield GoodsItem(url=href,insert_time=str(datetime.datetime.now()))
            elif netloc == "go.1688.com" and 'supplier' in path:
                yield IndexItem(url=href,insert_time=str(datetime.datetime.now()))
                #yield scrapy.Request(href,callback=self.parse_index)


        #parse shop
        for href in response.xpath('//*[@id="listbody"]/div[@class="supplier-list"]/div[@class="supplier"]/div[@class="title p-margin"]//a/@href').extract():
            if not href.startswith("http://"):
                continue 
            scheme, netloc, path, params, query, fragment = parse_url(href)
            shop_url = "%s://%s/"%(scheme,netloc)
            self.log('[parse_index] found shop %s from %s'%(shop_url,response.url),level=scrapy.log.INFO)
            yield ShopItem(url=shop_url,insert_time=str(datetime.datetime.now()))


        
        #next page    
        scheme, netloc, path, params, query, fragment = parse_url(response.url)
        qs = parse_query(query)
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

            yield scrapy.Request(urlparse.urlunparse( (scheme, netloc, path, params,query,"")),callback=self.parse_index)
