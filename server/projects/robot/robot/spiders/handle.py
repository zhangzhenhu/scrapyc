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
        yield scrapy.Request("http://thesis.lib.ncu.edu.tw/browse-title",callback=self.parse)
        yield scrapy.Request("http://ir.lib.ncu.edu.tw/browse-title",callback=self.parse)
        yield scrapy.Request("http://nchuir.lib.nchu.edu.tw/browse-title",callback=self.parse)
        yield scrapy.Request("http://hermes-ir.lib.hit-u.ac.jp/rs/browse-title",callback=self.parse)
        # yield scrapy.Request("")
        for item in super(HandleSpider, self).start_requests():
            yield item        


    def parse(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        base_url  = get_base_url(response)
        for href in response.xpath('//table/tr/td/strong/a/@href').extract():
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
            #self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)
            #yield scrapy.Request(url=abs_url,callback=self.parse)

        #解析pdf
        for href in response.xpath('//table[@class="object_table"]/tr/td[4]/a/@href').extract():
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
            #self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)
            #yield scrapy.Request(url=abs_url,callback=self.parse)

        #解析翻页
        for href in response.xpath('//table/tr/td/table/tr/td/a/@href').extract():
            if ("page=" not in href  and "browse-title?top=" not in href ) or "itemsPerPage=" in href:
                continue

            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
            #self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)
            yield scrapy.Request(url=abs_url,callback=self.parse)


class HandleCNSpider(base.RobotSpider):
    name = "handle_cn"

    allowed_domains = []
    start_urls = [    ]
    def start_requests(self):

        yield scrapy.Request("http://dspace.imech.ac.cn/browse?type=dateissued",callback=self.parse_first)
        # yield scrapy.Request("http://thesis.lib.ncu.edu.tw/browse-title",callback=self.parse)
        # yield scrapy.Request("http://ir.lib.ncu.edu.tw/browse-title",callback=self.parse)
        # yield scrapy.Request("http://nchuir.lib.nchu.edu.tw/browse-title",callback=self.parse)
        # yield scrapy.Request("http://hermes-ir.lib.hit-u.ac.jp/rs/browse-title",callback=self.parse)
        # yield scrapy.Request("")
        for item in super(HandleCNSpider, self).start_requests():
            yield item        


    def parse_first(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return 
        ret = re.search("var totalItemCount = (\d+);",response.body)
        if ret:
            totalItemCount = int(ret.groups()[0])
        offset = 0
        while offset < totalItemCount:
            yield scrapy.Request("http://dspace.imech.ac.cn/browse?order=DESC&rpp=100&sort_by=2&year=&offset=%d&type=dateissued"%offset,callback=self.parse)
            offset += 100

    def parse(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return 
        base_url  = get_base_url(response)
        for href in response.xpath('//form[@name="itemlist"]/table/tr[@class="itemLine"]/td/span/a/@href').extract():
            relative_url = href
            if relative_url.startswith("/simple-search?"):
                continue

            abs_url =urljoin_rfc(base_url,relative_url.split(":",1)[0])
            yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
            #self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)
            #yield scrapy.Request(url=abs_url,callback=self.parse)


