# -*- coding: utf-8 -*-
import scrapy
from robot.items import UrlItem
from w3lib.url import urljoin_rfc

class OneSpider(scrapy.Spider):
    name = "one"
    allowed_domains = []
    start_urls = (
        #'http://www.scrapy.cfg/',
    )
    # def __init__(self,*args, **kwargs):
    #     super(OneSpider, self).__init__(*args, **kwargs)
    #     self._kwargs = kwargs

    def start_requests(self):

        with open(self.settings['input']) as f:
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                url = line.split("\t")[0]
                if "://" not in url[:10]:
                    url = "http://" + url
                elif  url.split("://",1)[0]  not in ["http","https"]:
                    continue
                yield scrapy.Request(url)
        
    def parse(self, response):
        self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status != 200 :
            yield response.request 
            return
        depth = response.meta.get("depth",1) 
        for href in response.xpath("//a/@href").extract():
            href = href.strip()
            if href.startswith("javascript:"):
                continue
            abs_url =urljoin_rfc(response.url,href)
            yield UrlItem(url=abs_url,fromurl=response.url)
            if depth < 2:
                depth += 1
                yield scrapy.Request(abs_url,meta={"depth":depth})

