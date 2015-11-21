# -*- coding: utf-8 -*-
"""
示例爬虫

Authors: acmtiger@gmail.com
Date:    2015/11/16 9:42
"""
import scrapy
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc
from scrapy import signals


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["sina.cn"]
    start_urls = [
        "http://news.sina.cn/",
        "http://news.sina.cn/?vt=4&pos=3&sa=t124d8889597v84"
    ]

    def __init__(self, *args, **kwargs):
        """
        发布到scrapyc的爬虫需要添加带有*args, **kwargs参数的__init__函数
        因为scrapyc平台会通过命令行传入一些参数给spider，在这里接收
        Args:
            *args: 传入的value型参数
            **kwargs: 传入的name=value型参数

        Returns:

        """
        self.setting = kwargs
        # self.crawler.signals.connect(self.spider_idle,signals.spider_idle)
        pass

    def parse(self, response):
        base_url = get_base_url(response)
        for sel in response.xpath('//a/@href'):
            relative_url = sel.extract()
            abs_url = urljoin_rfc(base_url, relative_url)
            print abs_url
            # yield scrapy.Request(abs_url,callback=self.parse)

    def spider_idle(self, spider):

        if spider == self:
            return False
        return True
