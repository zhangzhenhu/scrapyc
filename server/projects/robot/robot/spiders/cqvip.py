#encoding=UTF8
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc

from scrapy import signals
from robot.items import NimeiItem
from robot.spiders import base
import scrapy
from scrapyc.server.utils.url import get_url_site,get_url_scheme
import urlparse
import re
import datetime
import string

class RobotSpider(base.RobotSpider):
    name = "cqvip"

    allowed_domains = []
    start_urls = [    ]
    def start_requests(self):

        # yield scrapy.Request("http://www.cqvip.com/journal/63.shtml",callback=self.parse_index)
        # yield scrapy.Request("http://www.cqvip.com/journal/1.shtml",callback=self.parse_index)
        # yield scrapy.Request("http://www.cqvip.com/journal/67.shtml",callback=self.parse_index)
        # yield scrapy.Request("http://www.cqvip.com/journal/64.shtml",callback=self.parse_index)
        # yield scrapy.Request("http://www.cqvip.com/journal/66.shtml",callback=self.parse_index)
        # yield scrapy.Request("")
        for item in super(RobotSpider, self).start_requests():
            yield item        
    #PATTERN1=re.compile(".*thread\-\d+\-\d+\-\d+\.html.*")

    def parse(self,response):

        if "journal" in response.url.lower():
            for item in self.parse_index(response):
                yield item 
        else:
            for item in self.parse_content(response):
                yield item
        

    def parse_index(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        base_url  = get_base_url(response)
        count = 0
        for href in response.xpath("//a/@href").extract():
            if re.match("/[Jj]ournal/\d+(_\d+)?\.shtml",href)   :
                relative_url = href
                abs_url =urljoin_rfc(base_url,relative_url)
                #yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
                self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)
                yield scrapy.Request(url=abs_url,callback=self.parse_index)

            #解析期刊首页
            if "QK" in href or "qk" in href:
                relative_url = href
                abs_url =urljoin_rfc(base_url,relative_url)
                self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)
                #yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
                yield scrapy.Request(url=abs_url,callback=self.parse_content)   
                count += 1
        self.log("Fuck %s %d"%(response.url,count),level=scrapy.log.INFO)


    def parse_content(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        base_url  = get_base_url(response)
        #解析文章
        for href in response.xpath("//em/a/@href").extract():
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)            
            yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
            #self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)
        #解析历史期刊首页
        for href in response.xpath("//ol[@class='date']/li/a/@href").extract():
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            yield scrapy.Request(url=abs_url,callback=self.parse_content)            
            yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
            #self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)


       