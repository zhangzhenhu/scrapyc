import scrapy
import datetime
import time
#from alibaba import settings
import re
import json
import urlparse
import json
from scrapy import log
from alibaba.items import ShopItem,GoodsItem,IndexItem
#from scrapy.conf import settings
from scrapy.utils.url import parse_url
import urlparse
from scrapy.contrib.spiders import CrawlSpider, Rule
import lxml.html
import lxml.etree


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

def unparse_query(qs):
    query = ""
    for k,v in qs.items():
        query += "&%s=%s"%(k,v)
    if query:
        query = query[1:]
    return query

class ShopSpider(scrapy.Spider):
    name = "shop"
    allowed_domains = [ ]
    start_urls = []
    
    def __init__(self,*args, **kwargs):
        super(ShopSpider, self).__init__(*args, **kwargs)
        self._kwargs = kwargs



        self.m_rules=[
            (re.compile('^http://jinpai\.1688\.com/'),self.parse_jinpai),
            (re.compile('^http://go\.1688\.com/supplier/'),self.parse_index),
            (re.compile('^http://s.1688.com/caigou/offer_search.htm'),self.parse_caigou),
            #(re.compile('^http://s.1688.com/selloffer/offer_search.htm'),self._parse_ziyuan_list),
            (re.compile('^http://s.1688.com/caigou/rpc_offer_search.jsonp'),self.pase_jsonp),
             
            ]



    def start_requests(self):

        requests = []
        #requests.append(scrapy.Request('http://jinpai.1688.com/',callback=self.parse_jinpai))
        #requests.append(scrapy.Request('http://go.1688.com/supplier/gold_supplier.htm',callback=self.parse_index))
        requests.append(scrapy.Request('http://s.1688.com/caigou/offer_search.htm?keywords=%C0%AD%C1%B4&n=y&from=industrySearch&industryFlag=jicai'))
        return requests


    def parse(self,response):
        self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status != 200 :
            yield response.request 
            return        
        for rule in self.m_rules:
            if rule[0].match(response.url):
                return rule[1](response)
                #print rule
    
    def parse_jinpai(self, response):

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
                yield scrapy.Request(href)


        pass

    def parse_index(self,response):
 
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
                yield scrapy.Request(href)


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
        self.log('[parse_index] pageStart:%d pageCount:%d %s'%(pageStart,pageCount,response.url),level=scrapy.log.INFO)
        if pageStart < pageCount:
            qs['pageStart'] = str(pageStart+1)
            qs['pageCount'] = str(pageCount)

            query = unparse_query(qs)
            yield scrapy.Request(urlparse.urlunparse( (scheme, netloc, path, params,query,"")))



    
    def parse_caigou(self,response):
        ''' parse like this :http://s.1688.com/caigou/offer_search.htm?.....'''
        #parse category
        for href in response.xpath('//a/@href').extract():
            if not href.startswith("http://s.1688.com/caigou/offer_search.htm?"):
                continue 
            yield IndexItem(url=href,insert_time=str(datetime.datetime.now()))
            #yield scrapy.Request(href)


        #parse shop
        for href in response.xpath('//li[@class="sm-offerItem"]/div[@class="sm-offerItem-alitalk"]//a[2]/@href').extract():
            if not href.startswith("http://"):
                continue 
            
            shop_url = href+"/"
            self.log('[parse_index] found shop %s from %s'%(shop_url,response.url),level=scrapy.log.INFO)
            yield ShopItem(url=shop_url,insert_time=str(datetime.datetime.now()))


        
        #next page    
        scheme, netloc, path, params, query, fragment = parse_url(response.url)
        qs = parse_query(query)
        keywords = qs.get('keywords')
        totalPage= int(response.xpath('//*[@id="content"]/div[1]/div[1]/div[1]/span/em/text()'))
        if not keywords:
            return
        
        jsonrpc_url='http://s.1688.com/caigou/rpc_offer_search.jsonp?keywords=%(keywords)s&n=y&async=true&asyncCount=60&startIndex=0&qrwRedirectEnabled=false&offset=0&isWideScreen=false&controls=_template_%3Aofferresult%2CjicaiOfferResult.vm%7C_moduleConfig_%3AshopwindowResultConfig%7C_name_%3AofferResult&token=237250634&beginPage=3&callback=%(callback)s&beginPage=%(beginPage)d&%(totalPage)d'%{"callback":self.jsonp_callback,"beginPage":page,"keywords":keywords,"totalPage":totalPage}

        
        yield scrapy.Request(jsonrpc_url)


    jsonp_callback = 'jQuery17207419333776924759_1420532315652'
    _regex = re.compile(r'\\(?![/u"])')

    def pase_jsonp(self,response):
        fixedcontent = regex.sub(r"\\\\", response.body)
        rep = json.loads(fixedcontent[len(jsonp_callback):-1].decode("GBK"))
        if rep["hasError"] == True:
            self.log("[pase_jsonp] Error:%s %s"%(rep["message"],response.url),level=scrapy.log.ERROR)
            return
        content = rep["content"]["offerResult"]["html"]
        tree=lxml.html.fromstring(content)
        #pdb.set_trace()
        #parse shop
        for href in tree.xpath('//li[@class="sm-offerItem"]/div[@class="sm-offerItem-alitalk"]//a[2]/@href').extract():
            if not href.startswith("http://"):
                continue 
            shop_url = href+"/"
            self.log('[pase_jsonp] found shop %s from %s'%(shop_url,response.url),level=scrapy.log.INFO)
            yield ShopItem(url=shop_url,insert_time=str(datetime.datetime.now()))

        #nextpage
        scheme, netloc, path, params, query, fragment = parse_url(response.url)
        qs = parse_query(query)
        try:
            totalPage = int(qs.get('totalPage'))
            beginPage = int(qs.get('beginPage'))
        except Exception, e:
            self.log("[pase_jsonp] %s"%e,level=scrapy.log.ERROR)
            return
       
        if not beginPage >= totalPage:
            return
        qs['beginPage'] = beginPage + 1
        query = unparse_query(qs)
        yield scrapy.Request(urlparse.urlunparse( (scheme, netloc, path, params,query,fragment)))
        
        