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

    def parse(self, response):
        self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status != 200 :
            yield response.request 
            return 
         for href in div.xpath("//a/@href").extract():
            href = href.strip()
            if href.startswith("javascript:"):
                continue
            abs_url =urljoin_rfc(response.url,href)

