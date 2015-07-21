#encoding=utf8
#Description:
#学术项目，例行抓取一些pdf文档的链接。

import scrapy
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc

from scrapy import signals
from robot.items import NimeiItem
from robot.spiders import base
from scrapy.utils.misc import load_object
from scrapyc.server.utils.url import get_url_site,get_url_scheme
import json


class RobotSpider(base.RobotSpider):
    name = "pdf"
    allowed_domains = []
    start_urls = [    ]
    parses = {}


    def start_requests(self):
        yield scrapy.Request("http://140.127.82.35/ETD-db/ETD-browse/browse?first_letter=all&browse_by=last_name",callback=self.parse0)

        for item in super(RobotSpider, self).start_requests():
            yield item

    def parse(self, response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        for a in response.xpath('//a'):
            text = a.xpath("u/text()").extract()
            if len(text) !=1:
                continue
            text = text[0]
            if "PDF" not in text:
                continue
            href = a.xpath("@href").extract()
            if len(href) != 1:
                continue
            href = href[0]
            if href == "#" or href.startswith("javascript") and len( a.xpath("@onclick").extract()) ==1:
                onclick =  a.xpath("@onclick").extract()[0]
                onclick = onclick.split(",")
                if len(onclick) < 2:
                    continue
                id = onclick[1].split(")",1)[0].replace("'","")
                pdf = response.url.split("/CN/",1)[0] + "/CN/article/downloadArticleFile.do?attachType=PDF&id="+id
            elif len( a.xpath("@href").extract()) ==1:
                href = a.xpath("@href").extract()[0]
                abs_url =urljoin_rfc(response.url,href)
                pdf = abs_url

            #url = "http://www.zjnyxb.cn/CN/article/downloadArticleFile.do?attachType=PDF&id="+id
            #print pdf
            yield self.baidu_rpc_request({"url":pdf,"src_id":4})                             

    def parse0(self, response):
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

