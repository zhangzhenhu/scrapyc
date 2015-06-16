import scrapy
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc
import re
from scrapy import signals
from robot.items import NimeiItem
from robot.spiders import base
from scrapy.utils.misc import load_object
from scrapy.utils.response import body_or_str
from scrapyc.server.utils.url import get_url_site,get_url_scheme
import json


class SiteMapSpider(base.RobotSpider):
    name = "sitemap"
    allowed_domains = []
    start_urls = [    ]
    parses = {}
    RE_PATTERN_LOC=re.compile(r"(<%s[\s>])(.*?)(</%s>)" % ('loc', 'loc'), re.DOTALL)
    def start_requests(self):
        yield scrapy.Request("http://wenwen.sogou.com/sitemap_index.xml",callback=self.parse_index)

        for item in super(SiteMapSpider, self).start_requests():
            yield item

    def parse_sitemap(self, response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
       
        text = body_or_str(response)
       
        for match in self.RE_PATTERN_LOC.finditer(text):
            url = match.group(2)
            yield self.baidu_rpc_request({"url":url,"src_id":4})
            yield NimeiItem(url=url,furl=response.url)
    
    def parse_index(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        text = body_or_str(response)
        for match in self.RE_PATTERN_LOC.finditer(text):
            url = match.group(2)
            yield scrapy.Request(url=url,callback=self.parse_sitemap)


    def spider_idle(self,spider):

        if spider==self:
            return False
        return True
