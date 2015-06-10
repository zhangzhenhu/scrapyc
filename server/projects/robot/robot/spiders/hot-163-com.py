import scrapy
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc

from scrapy import signals
from robot.items import NimeiItem
from scrapy.utils.misc import load_object
from scrapyc.server.utils.url import get_url_site,get_url_scheme
import json


class RobotSpider(robot.spiders.robot.RobotSpider):
    name = "hot-163-com"
    allowed_domains = []
    start_urls = [    ]
    parses = {}



    def parse(self, response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        
        site = get_url_site(response.url)

        base_url  = get_base_url(response)
        for sel in response.xpath('//a/@href'):
            relative_url = sel.extract()
            abs_url =urljoin_rfc(base_url,relative_url)
            #print abs_url
            schema = get_url_scheme(abs_url)
            if schema not in ["http","https"]:
                continue            
            site = get_url_site(abs_url)
            yield NimeiItem(url=abs_url,furl=response.url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4})




    def spider_idle(self,spider):

        if spider==self:
            return False
        return True
