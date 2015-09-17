#encoding=UTF8
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
import string

class RobotSpider(base.RobotSpider):
    name = "wanfangdata"

    allowed_domains = []
    start_urls = [    ]
    def start_requests(self):

        # yield scrapy.Request("http://c.wanfangdata.com.cn/Periodical.aspx")
        # yield scrapy.Request("http://c.wanfangdata.com.cn/LastUpdatedPeriodical.aspx")
        # for letter in string.ascii_uppercase:
        #     url = "http://c.wanfangdata.com.cn/PeriodicalLetter.aspx?NodeID=%s"%letter
        #     yield scrapy.Request(url,self.parse_index)

        for item in super(RobotSpider, self).start_requests():
            yield item        
    #PATTERN1=re.compile(".*thread\-\d+\-\d+\-\d+\.html.*")

    def parse_index(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            yield scrapy.Request(url=response.url,callback=self.parse_index)
            return
        base_url  = get_base_url(response)
        #解析期刊首页
        count = 0
        for href in response.xpath("//div[@id='divperilist']/ul/li/a/@href").extract():
            if href.startswith("Rss.ashx?"):
                continue
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            #self.log("Parse %s %s"%(response.url,abs_url),level=scrapy.log.INFO)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
            yield scrapy.Request(url=abs_url,callback=self.parse_content)
            count += 1
        self.log("Fuck %s %d"%(response.url,count),level=scrapy.log.INFO)

        #解析索引页翻页
        for href in response.xpath("//div[@id='divperilist']/table//a/@href").extract():
            if "PageNo" not in href:
                continue
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            self.log("Parse %s %s"%(response.url,abs_url),level=scrapy.log.INFO)
            yield scrapy.Request(url=abs_url,callback=self.parse_index)
            #yield self.baidu_rpc_request({"url":abs_url,"src_id":4},furl=response.url)

    def parse_content(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            yield scrapy.Request(url=response.url,callback=self.parse_content)
            return
        base_url  = get_base_url(response)
        #解析文章
        for href in response.xpath("//div[@id='wrap3']//a[@class='qkcontent_name']/@href").extract():
            #self.log("Parse %s %s"%(response.url,href),level=scrapy.log.INFO)
            yield self.baidu_rpc_request({"url":href,"src_id":22},furl=response.url)

        #解析历史期刊首页
        for href in response.xpath("//div[@id='wrap3']//ul[@class='new_ul5']/li/p/a/@href").extract():
            relative_url = href
            if '2015' in relative_url:
                abs_url =urljoin_rfc(base_url,relative_url)
                yield scrapy.Request(url=abs_url,callback=self.parse_content)            
        #     yield self.baidu_rpc_request({"url":abs_url,"src_id":4},furl=response.url)
        #     self.log("Parse %s %s"%(response.url,abs_url),level=scrapy.log.INFO)


    def parse(self,response):

        for item in self.parse_content(response):
            yield item
        return
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        base_url  = get_base_url(response)
        for href in response.xpath('//a/@href').extract():
            if not self.is_valid_url(href):
                continue
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            #yield self.baidu_rpc_request({"url":abs_url,"src_id":4})
            for pattern in ["Periodical-[\w\-0-9]+\.aspx$","periodical/[\w\-0-9]+/\d{4}-\d+\.aspx","PeriodicalSubject.aspx\?NodeId=[\w\.0-9&=]+"]:
                if re.search(pattern,relative_url):
                    yield scrapy.Request(url=abs_url)
                    self.log("Parse %s %s"%(response.url,abs_url),level=scrapy.log.INFO)

       