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

class RobotSpider(base.RobotSpider):
    name = "wccdaily.scol.com.cn"

    allowed_domains = []
    start_urls = [    ]
    def start_requests(self):

        start = datetime.date(2012,7,16)
        today = datetime.date.today()
        while start <= today:
            url = "http://wccdaily.scol.com.cn/shtml/hxdsb/%s/index.shtml"%start.strftime("%Y%m%d")
            yield scrapy.Request(url)
            start += datetime.timedelta(days=1)
        for item in super(RobotSpider, self).start_requests():
            yield item        
    #PATTERN1=re.compile(".*thread\-\d+\-\d+\-\d+\.html.*")
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
        for sel in response.xpath('//*/@onclick').extract():
            if  not sel.startswith("gotourl"):
                continue
            relative_url = sel.split("'")[1]
            abs_url =urljoin_rfc(base_url,relative_url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4})
            