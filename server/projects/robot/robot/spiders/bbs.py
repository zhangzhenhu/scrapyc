from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc

from scrapy import signals
from robot.items import NimeiItem
import scrapy
from scrapyc.server.utils.url import get_url_site,get_url_scheme



class RobotSpider(robot.spiders.robot.RobotSpider):
    name = "bbs"

    allowed_domains = []
    start_urls = [    ]


    def parse(self,response):

        base_url  = get_base_url(response)
        for sel in response.xpath('//a/@href'):
            relative_url = sel.extract()
            abs_url =urljoin_rfc(base_url,relative_url)
            schema = get_url_scheme(abs_url)
            if schema not in ["http","https"]:
                continue  

            yield NimeiItem(url=abs_url,furl=response.url)
            if relative_url.startswith("forum_") or relative_url.startswith("forum-") or relative_url.startswith("/archives/"):
                
                yield scrapy.Request(abs_url)
            