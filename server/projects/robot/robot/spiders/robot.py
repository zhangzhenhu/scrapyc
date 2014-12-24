import scrapy
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc

from scrapy import signals
class RobotSpider(scrapy.Spider):
    name = "robot"
    allowed_domains = ["sina.cn"]
    start_urls = [
        "http://news.sina.cn/",
        "http://news.sina.cn/?vt=4&pos=3&sa=t124d8889597v84"
    ]
    def __init__(self):
        self.crawler.signals.connect(self.spider_idle,signals.spider_idle)
        pass
    def parse(self, response):
        base_url  = get_base_url(response)
        for sel in response.xpath('//a/@href'):
            relative_url = sel.extract()
            abs_url =urljoin_rfc(base_url,relative_url)
            print abs_url
            #yield scrapy.Request(abs_url,callback=self.parse)
    def spider_idle(self,spider):

        if spider==self:
            return False
        return True
