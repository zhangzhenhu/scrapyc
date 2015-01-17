# -*- coding: utf-8 -*-
import scrapy


class OneSpider(scrapy.Spider):
    name = "one"
    allowed_domains = ["scrapy.cfg"]
    start_urls = (
        'http://www.scrapy.cfg/',
    )

    def parse(self, response):
        pass
