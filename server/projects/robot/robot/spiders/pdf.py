#encoding=utf8
#Description:
#学术项目，例行抓取一些pdf文档的链接。

import scrapy
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc,safe_url_string

from scrapy import signals
from robot.items import NimeiItem
from robot.spiders import base
from scrapy.utils.misc import load_object
from scrapyc.server.utils.url import get_url_site,get_url_scheme
import json
import urllib


class RobotSpider(base.RobotSpider):
    name = "pdf"
    allowed_domains = []
    start_urls = [    ]
    parses = {}


    def start_requests(self):
        #yield scrapy.Request("http://140.127.82.35/ETD-db/ETD-browse/browse?first_letter=all&browse_by=last_name",callback=self.parse1)
        #yield scrapy.Request("http://202.116.42.39/xxdy/ckwx/index.html",callback=self.parse_cameo)
        #yield scrapy.Request("http://202.116.42.39/xxdy/ckwx/index2.html",callback=self.parse_cameo)
        #yield scrapy.Request("http://www.zgyszz.com/qklist/li0s/p1.html",callback=self.parse_zgyszz)
        
        #yield scrapy.Request("http://tszy.bfa.edu.cn/drms_bfa/portal/beiying/index109.113_list.jsp?currPath=%D1%A7%BF%C6%CD%BC%CA%E9%C7%E9%B1%A8/%B5%E7%D3%B0%D1%A7%BF%C6%B5%C4%B5%E7%D7%D3%D7%CA%D4%B4%D0%C5%CF%A2/hylw_jm",callback=self.parse2)

        # for i in range(1,2919):
        #     url = "http://cameo.net.cn/List.asp?ces=C&pageNO=%d"%i
        #     yield scrapy.Request(url,callback=self.parse_cameo)
        #     yield self.baidu_rpc_request({"url":url,"src_id":4}) 
        
        #yield scrapy.Request("http://cf.lcchina.org.cn/",callback=self.parse_all)


        # for i in range(1,1501):
        #     url = "http://tkuir.lib.tku.edu.tw:8080/dspace/browse-title?itemsPerPage=50&page=%d"%i
        #     yield scrapy.Request(url,callback=self.parse_cameo)
        #     yield self.baidu_rpc_request({"url":url,"src_id":4}) 
        
        # url = "http://tkuir.lib.tku.edu.tw:8080/dspace/browse-title?itemsPerPage=50"
        # yield scrapy.Request(url,callback=self.parse_cameo)
        # yield self.baidu_rpc_request({"url":url,"src_id":4}) 
        # i = 0
        # while i < 73334:
            
        #     url = "http://dspace.lib.ntnu.edu.tw/browse?type=title&sort_by=1&order=ASC&rpp=100&etal=-1&null=&offset=%d"%i
        #     i += 100
        #     yield scrapy.Request(url,callback=self.parse_cameo)
        #     yield self.baidu_rpc_request({"url":url,"src_id":4}) 
    

        for item in super(RobotSpider, self).start_requests():
            yield item

    def parse(self, response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        count = 0
        for a in response.xpath('//a'):
            text = a.xpath("u/text()").extract()
            if len(text) !=1:
                text = a.xpath("text()").extract()
            if len(text) !=1:
                continue
            text = text[0]
            if "PDF" not in text:
                continue
            href = a.xpath("@href").extract()
            if len(href) != 1:
                continue
            href = href[0]
            if  ( href == "#" or href.startswith("javascript") ) and len( a.xpath("@onclick").extract()) ==1:
                onclick =  a.xpath("@onclick").extract()[0]
                onclick = onclick.split(",")
                if len(onclick) < 2:
                    continue
                id = onclick[1].split(")",1)[0].replace("'","")
                if  "/CN/" in response.url:
                    pdf = response.url.split("/CN/",1)[0] + "/CN/article/downloadArticleFile.do?attachType=PDF&id="+id
                elif "/EN/" in response.url:
                    pdf = response.url.split("/EN/",1)[0] + "/EN/article/downloadArticleFile.do?attachType=PDF&id="+id
                else:
                    continue
            elif  href != "#" and not href.startswith("javascript"):
                
                abs_url =urljoin_rfc(response.url,href)
                pdf = abs_url
            else:
                continue
            #url = "http://www.zjnyxb.cn/CN/article/downloadArticleFile.do?attachType=PDF&id="+id
            #print pdf
            yield self.baidu_rpc_request({"url":pdf,"src_id":4})
            count += 1                         

        base_url  = get_base_url(response)
        for sel in response.xpath('//a/@href'):
            relative_url = sel.extract().encode(response.encoding)
            if relative_url.startswith("javascript:") or relative_url=="#":
                continue         
            abs_url = urljoin_rfc(base_url,relative_url)
            abs_url = safe_url_string(abs_url,encoding=response.encoding)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4}) 
        self.log("PDF %s %d"%(response.url,count),level=scrapy.log.INFO)

    def parse1(self, response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        for href in response.xpath("//td/a/@href").extract():
            href = href.split("?URN=")
            if len(href) != 2:
                continue
            etd = href[1]
            pdf = "140.127.82.35/ETD-db/ETD-search/getfile?URN=%s&filename=%s.pdf"%(etd,etd)
            yield self.baidu_rpc_request({"url":pdf,"src_id":4})

        base_url  = get_base_url(response)
        for sel in response.xpath('//a/@href'):
            relative_url = sel.extract().encode(response.encoding)
            abs_url = urljoin_rfc(base_url,relative_url)
            abs_url = safe_url_string(abs_url,encoding=response.encoding)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4}) 



    def parse2(self, response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        base_url  = get_base_url(response)
        for sel in response.xpath('//table/tr/td/div/a/@href'):
            relative_url = sel.extract().encode(response.encoding)
            abs_url = urljoin_rfc(base_url,relative_url)
            abs_url = safe_url_string(abs_url,encoding=response.encoding)
        
            if relative_url.endswith(".pdf") or relative_url.endswith(".doc"):
                yield self.baidu_rpc_request({"url":abs_url,"src_id":4}) 
            elif  relative_url.startswith("?currPath=") :
                yield scrapy.Request(url=abs_url,callback=self.parse2)

    def parse_cameo(self, response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        base_url  = get_base_url(response)
        for sel in response.xpath('//a/@href'):
            relative_url = sel.extract().encode(response.encoding)
            abs_url = urljoin_rfc(base_url,relative_url)
            abs_url = safe_url_string(abs_url,encoding=response.encoding)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4}) 

    def parse_all(self, response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        base_url  = get_base_url(response)
        base_site = get_url_site(base_url)

        for sel in response.xpath('//a/@href'):
            relative_url = sel.extract().encode(response.encoding)
            if relative_url.startswith("javascript:") or relative_url=="#":
                continue            
            abs_url = urljoin_rfc(base_url,relative_url)
            abs_url = safe_url_string(abs_url,encoding=response.encoding)

            filename = abs_url.split("?")[0].split("/")[-1]
            if filename :
                ctype  = filename.split(".")[-1].lower() 
            else:
                ctype = None
            if ctype in ["jpeg","jpg","swf","rar","zip","gz","gif","mov","png","bmp","exe","pps","db","txt","pptx",'xls',"ppt","xlsx"]:
                continue

            yield self.baidu_rpc_request({"url":abs_url,"src_id":4})

            site = get_url_site(abs_url)
            if site != base_site:
                continue
            if ctype in ["pdf","doc","docx","rtf",]:
                continue
            yield scrapy.Request(url=abs_url,callback=self.parse_all)
           

    def parse_zgyszz(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return

        #base_site = get_url_site(base_url)
        if  "qklist/show-" in response.url:
            base_url  = get_base_url(response)

            downLink = response.xpath("//div[@id='down']//a/@onclick").extract()[0]
            relative_url = downLink.split("'")[1]

            abs_url = urljoin_rfc(base_url,relative_url)
            yield scrapy.Request(abs_url,callback=self.parse_zgyszz)

            yield self.baidu_rpc_request({"url":abs_url,"src_id":4})
            
            return
        if '/upload/qklist/' in response.url:
            yield self.baidu_rpc_request({"url":response.url,"src_id":4})
            return

        base_url  = response.url
        for sel in response.xpath("//div[@class='main_box']//table/tr[1]/td/a/@href"):
            relative_url = sel.extract().encode(response.encoding)
            if relative_url.startswith("javascript:") or relative_url=="#":
                continue            
            abs_url = urljoin_rfc(base_url,relative_url)
            abs_url = safe_url_string(abs_url,encoding=response.encoding)
            request = scrapy.Request(abs_url,callback=self.parse_zgyszz)
            #request.meta["dont_redirect"] = True
            yield request
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4})
        
        for sel in response.xpath("//div[@class='flickr']/a/@href"):
            relative_url = sel.extract().encode(response.encoding)
            if relative_url.startswith("javascript:") or relative_url=="#":
                continue            
            abs_url = urljoin_rfc(base_url,relative_url)
            abs_url = safe_url_string(abs_url,encoding=response.encoding)
            request = scrapy.Request(abs_url,callback=self.parse_zgyszz)
            yield request
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4})


