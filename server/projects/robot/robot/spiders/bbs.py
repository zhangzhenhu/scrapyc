from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc

from scrapy import signals
from robot.items import NimeiItem
from robot.spiders import base
import scrapy
from scrapyc.server.utils.url import get_url_site,get_url_scheme



class RobotSpider(base.RobotSpider):
    name = "bbs"

    allowed_domains = []
    start_urls = [    ]


    def parse(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return

        base_url  = get_base_url(response)
        for sel in response.xpath('//a/@href'):
            relative_url = sel.extract()
            if relative_url.startswith("javascript:"):
                continue

            abs_url =urljoin_rfc(base_url,relative_url)
            schema = get_url_scheme(abs_url)
            if schema not in ["http","https"]:
                continue  

            #yield NimeiItem(url=abs_url,furl=response.url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4})
            if relative_url.startswith("forum_") or relative_url.startswith("forum-") or relative_url.startswith("/archives/") or relative_url.startswith("forumdisplay.php?fid=") or relative_url.startswith("forum.php?mod=forumdisplay&fid="):
                
                yield scrapy.Request(abs_url)
            