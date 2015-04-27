import scrapy
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc

from scrapy import signals
from robot.items import NimeiItem
class RobotSpider(scrapy.Spider):
    name = "robot"
    allowed_domains = ["sina.cn"]
    start_urls = [
        "http://news.sina.cn/",
        "http://news.sina.cn/?vt=4&pos=3&sa=t124d8889597v84"
    ]
    def start_requests(self):
        self.crawler.signals.connect(self.spider_idle,signals.spider_idle)
        for url in self.start_urls:
            req =  scrapy.Request(url,callback=self.parse)
            #req.meta["depth"] =  1
            yield req            
        pass
    def parse(self, response):
        base_url  = get_base_url(response)
        if "depth" in response.meta:
            depth = response.meta["depth"]
        else:
            depth = 1
        MAX_DEPTH =  self.settings.get("MAX_DEPTH",1)
        for sel in response.xpath('//a/@href'):
            relative_url = sel.extract()
            abs_url =urljoin_rfc(base_url,relative_url)
            #print abs_url

            yield scrapy.Request(abs_url,callback=self.parse)
            yield NimeiItem(url=abs_url,depth=0)
            # if depth < MAX_DEPTH:
            #     req =  scrapy.Request(abs_url,callback=self.parse)
            #     req.meta["depth"] = depth + 1
            #     yield req

    def spider_idle(self,spider):

        if spider==self:
            return False
        return True
