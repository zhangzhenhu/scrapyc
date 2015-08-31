#encoding=utf8
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

class WwwSpider(base.RobotSpider):
    name = "www.cnki.com.cn"

    allowed_domains = []
    start_urls = [    ]
    def start_requests(self):

        # yield scrapy.Request("http://cdmd.cnki.com.cn/Area/CDMDUnit-0002.htm")
        # yield scrapy.Request("http://cpfd.cnki.com.cn/Area/CPFDUnit-0009.htm")
        # yield scrapy.Request("http://cyfd.cnki.com.cn/catenav.aspx")
        # yield scrapy.Request("http://cdmd.cnki.com.cn/Area/CDMDUnitArticle-10183-2015-1.htm")
        yield scrapy.Request("http://www.cnki.com.cn/CJFD/CJFD_index.htm")
        # yield scrapy.Request("")
        # yield scrapy.Request("")
        # yield scrapy.Request("")
        for item in super(WwwSpider, self).start_requests():
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
        site = get_url_site(response.url)
        if site == "www.cnki.com.cn":
            self.parse_www(response)
    def parse_www(self,response):
        base_url  = get_base_url(response)
        for href in response.xpath('//a/@href').extract():
            if not self.is_valid_url(href):
                continue
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4})
            if "Journal" in relative_url or 'Navi' in relative_url:
                yield scrapy.Request(url=abs_url)

  

class CDmdSpider(base.RobotSpider):
    name = "cdmd.cnki.com.cn"

    allowed_domains = []
    start_urls = [    ]
    def start_requests(self):
        for i in range(1,42):
            yield scrapy.Request("http://cdmd.cnki.com.cn/Area/CDMDUnit-%04d.htm"%i,callback=self.parse_unit,headers={"Cache-Control":"no-cache","Cookie":"SID=110005; SID_cdmd=209021; CNZZDATA1356416=cnzz_eid%3D1750068259-1440478982-%26ntime%3D1440666594","Pragma":"no-cache"})
        for i in range(1,32):
            yield scrapy.Request("http://cpfd.cnki.com.cn/Area/CPFDUnit-%04d.htm"%i,callback=self.parse_unit)
        # yield scrapy.Request("")
        for item in super(CDmdSpider, self).start_requests():
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


    def parse_unit(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        site = get_url_site(response.url)
        base_url  = get_base_url(response)

        for href in response.xpath("//a[@class='zt_name']/@href").extract():
            # if not self.is_valid_url(href):
            #     continue
            if href == "#":continue
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4},furl=response.url)
            yield scrapy.Request(url=abs_url,callback=self.parse_cdmd)

    def parse_cdmd(self,response):
        base_url  = get_base_url(response)
        #解析期刊
        count = 0
        for href in response.xpath("//a[@class='zt_name']/@href").extract():
            if not self.is_valid_url(href):
                continue
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4},furl=response.url)
            count += 1
        #预测后续翻页
        if count in [15,21] and re.search("/Area/CDMDUnitArticle-\d+-\d{4}-\d+\.htm",response.url) :
            up = response.url.split("-")
            pageNo = up[-1].split('.')[0]
            pageNo = int(pageNo)+1
            abs_url = up[0]+"-"+up[1]+"-"+up[2]+"-"+str(pageNo)+".htm"
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4},furl=response.url)
            yield scrapy.Request(url=abs_url,callback=self.parse_cdmd)
            self.log("Nimei %s"%abs_url,level=scrapy.log.INFO)

        #解析历年索引页
        for href in response.xpath("//a[@class='content_gray02']/@href").extract():
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4},furl=response.url)
            yield scrapy.Request(url=abs_url,callback=self.parse_cdmd)

        #解析当前索引页的翻页
        # js = response.xpath("//table/tbody/tr/td/script").extract()
        # if js:
        #     js = js[0]
        #     articleTotal = re.search("var\s+articleTotal\s+=\s+(\d+);",js)
        #     countPerPage = re.search("var\s+countPerPage\s+=\s+(\d+);",js)
        #     curYear = re.search("var\s+curYear\s+=\s+(\d+);",js)
        #     curUnit = re.search("var\s+curUnit\s+=\s+(\d+);",js)
        #     if articleTotal and curUnit and countPerPage and curYear:
        #         articleTotal = int(articleTotal.groups()[0])
        #         countPerPage = int(countPerPage.groups()[0])
        #         curYear = curYear.groups()[0]
        #         curUnit = curUnit.groups()[0]
        #         totalPage = articleTotal / countPerPage
        #         if articleTotal % countPerPage != 0:
        #             totalPage += 1
        #         i = 1
        #         #print response.url,url,articleTotal,countPerPage,totalPage
        #         while i <= totalPage:
        #             url = "/Area/CDMDUnitArticle-%s-%s-%d.html"%(curUnit,curYear,i)
        #             #print response.url,url,articleTotal,countPerPage,totalPage
        #             i += 1                    