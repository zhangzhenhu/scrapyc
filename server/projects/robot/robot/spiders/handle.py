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

class HandleSpider(base.RobotSpider):
    name = "handle"

    allowed_domains = []
    start_urls = [    ]
    def start_requests(self):

        yield scrapy.Request("http://nccur.lib.nccu.edu.tw/browse-title",callback=self.parse)
        # yield scrapy.Request("")
        for item in super(HandleSpider, self).start_requests():
            yield item        


    def parse(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        base_url  = get_base_url(response)
        for href in response.xpath('//table[@class="object_table"]/tr/td/strong/a/@href').extract():
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4},furl=response.url)
            self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)
            yield scrapy.Request(url=abs_url,callback=self.parse)

        #解析pdf
        for href in response.xpath('//table[@class="object_table"]/tr/td[4]/a/@href').extract():
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4},furl=response.url)
            self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)
            #yield scrapy.Request(url=abs_url,callback=self.parse)

        #解析翻页
        for href in response.xpath('//table/tr/td/table/tr/td/a/@href').extract():
            if "page=" not in href:
                continue
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4},furl=response.url)
            self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)
            yield scrapy.Request(url=abs_url,callback=self.parse)


