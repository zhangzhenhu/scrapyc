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
    name = "sciencemeta"

    allowed_domains = []
    start_urls = [    ]
    def start_requests(self):

        for i in range(1,17):
            yield scrapy.Request("http://sciencemeta.net/index.php/index/index/journals?metaDisciplineExamples=&searchInitial=&journalsPage=%d#journals"%i)
       
        # yield scrapy.Request("http://cyfd.cnki.com.cn/catenav.aspx")
        # yield scrapy.Request("http://cdmd.cnki.com.cn/Area/CDMDUnitArticle-10183-2015-1.htm")
        # yield scrapy.Request("")
        # yield scrapy.Request("")
        # yield scrapy.Request("")
        # yield scrapy.Request("")
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
        count = 0
        for href in response.xpath('//a/@href').extract():
            if not self.is_valid_url(href):
                continue
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            if "/article/view/" in abs_url:
                count += 1
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4},response.url)
            if re.search("/issue/archive/\d+$",abs_url):
                yield scrapy.Request(url=abs_url)


        if count < 10:
            self.log("Fuck %s %d"%(response.url,count),level=scrapy.log.INFO)
        for href in response.xpath("//div[@id='content']//div[@class='sp_site_jlogo']//a/@href").extract():
            abs_url = href + "/issue/archive"
            
            yield scrapy.Request(url=abs_url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4},response.url)

       