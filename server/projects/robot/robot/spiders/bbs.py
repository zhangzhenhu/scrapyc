from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc,url_query_cleaner

from scrapy import signals
from robot.items import NimeiItem
from robot.spiders import base
import scrapy
from scrapyc.server.utils.url import get_url_site,get_url_scheme
import urlparse
import re

class RobotSpider(base.RobotSpider):
    name = "bbs"

    allowed_domains = []
    start_urls = [    ]
    PATTERN1=re.compile(".*thread\-\d+\-\d+\-\d+\.html.*")
    def parse_qsl(self,qs):

        for item in qs.split("&"):
            item = item.split("=",1)
            if len(item) == 2:
                yield (item[0],item[1])
            elif len(item) == 1 and item[0]:
                yield (item[0],"")
    def remove_param(self,url,rm_query=[]):
        up = urlparse.urlparse(url)
        n_query = ""
        for name,value in self.parse_qsl(up.query):
            if name not in rm_query and name :
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
            if "mod=redirect" in relative_url or "redirect.php" in relative_url:
                continue
                
            abs_url =urljoin_rfc(base_url,relative_url)
            schema = get_url_scheme(abs_url)
            if schema not in ["http","https"]:
                continue  

            #yield NimeiItem(url=abs_url,furl=response.url)
            abs_url = self.remove_param(abs_url,["extra","orderby","typeid","filter","sortid","searchsort","vk_payway_13","sid","recommend","digest"])


            if self.PATTERN1.match(abs_url):
                abs_url = re.sub("\-\d+\-\d+\.html.*","-1-1.html",abs_url,1)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4})
            if relative_url.startswith("forum_") or relative_url.startswith("forum-") or relative_url.startswith("/archives/") or relative_url.startswith("forumdisplay.php?fid=") or relative_url.startswith("forum.php?mod=forumdisplay&fid="):
                
                yield scrapy.Request(abs_url)
            