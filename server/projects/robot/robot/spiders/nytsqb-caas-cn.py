import scrapy
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc

from scrapy import signals
from robot.items import NimeiItem
from robot.spiders import base
from scrapy.utils.misc import load_object
from scrapyc.server.utils.url import get_url_site,get_url_scheme
import json


class RobotSpider(base.RobotSpider):
    name = "nytsqb.caas.cn"
    allowed_domains = []
    start_urls = [    ]
    parses = {}


    def start_requests(self):
        yield scrapy.Request("http://nytsqb.caas.cn/CN/volumn/current.shtml",callback=self.parse)
        
    def parse(self, response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        
        for href in response.xpath('//table//table//form//table//table//table//td[@class="J_VM"]/a[1]/@href').extract():
            if href.startswith("../abstract/abstract"):
                id = href[len("../abstract/abstract"):].replace(".shtml","")
                url = "http://nytsqb.caas.cn/CN/article/downloadArticleFile.do?attachType=PDF&id="+id
                yield self.baidu_rpc_request({"url":url,"src_id":4})

    def spider_idle(self,spider):

        if spider==self:
            return False
        return True
