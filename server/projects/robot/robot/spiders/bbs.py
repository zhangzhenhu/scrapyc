from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc

from scrapy import signals
from robot.items import NimeiItem
from robot.spiders import base
import scrapy
from scrapyc.server.utils.url import get_url_site,get_url_scheme
import urlparse


class RobotSpider(base.RobotSpider):
    name = "bbs"

    allowed_domains = []
    start_urls = [    ]
    def parse_qsl(self,qs):

        for item in qs.split("&"):
            item = item.split("=",1)
            if len(item) == 2:
                yield (item[0],item[1])
            else:
                yield (item[0],"")
    def remove_param(self,url,rm_query=[]):
        up = urlparse.urlparse(url)
        n_query = ""
        for name,value in self.parse_qsl(up.query):
            if name not in rm_query:
                n_query += "&%s=%s"%(name,value)
        return urlparse.urlunparse((up.scheme,up.netloc,up.path, up.params,n_query[1:],up.fragment))


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
            abs_url = self.remove_param(abs_url,["extra","orderby","typeid","filter",])
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4})
            if relative_url.startswith("forum_") or relative_url.startswith("forum-") or relative_url.startswith("/archives/") or relative_url.startswith("forumdisplay.php?fid=") or relative_url.startswith("forum.php?mod=forumdisplay&fid="):
                
                yield scrapy.Request(abs_url)
            