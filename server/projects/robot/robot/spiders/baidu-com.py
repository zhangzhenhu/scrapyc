# encoding = utf8
import scrapy
import json
from w3lib.url import url_query_parameter

__author__ = 'zhangzhenhu'


class BaiduSpider(scrapy.Spider):
    name = "baidu.com"
    allowed_domains = []
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(BaiduSpider, self).__init__(*args, **kwargs)
        self._kwargs = kwargs

    def start_requests(self):

        fname = self.settings.get("INPUT_FILE", None)
        if fname:
            with open(fname) as fh:
                for line in fh.readlines():
                    line = line.strip().split('\t')
                    url = line[0]
                    cate = line[1]
                    desc = line[2]
                    req = scrapy.Request(url, meta={"category": line[1], "desc": line[2]})
                    yield req
        url = self.settings.get("url", None)
        if url:
            yield scrapy.Request(url)
        for url in self.start_urls:
            req = scrapy.Request(url)
            # req.meta["depth"] =  1
            yield req
        for item in super(BaiduSpider, self).start_requests():
            yield item

    def parse(self, response):
        self.log("Crawled %s %d" % (response.url, response.status), level=scrapy.log.INFO)
        # self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            # self.log(response.headers,level=scrapy.log.INFO)
            yield scrapy.Request(response.url)
            return
        if response.__class__ != scrapy.http.HtmlResponse:
            return
        query = response.meta["category"] + " " + response.meta["desc"]  # url_query_parameter(response.url, 'wd')
        print query,
        for json_str in response.xpath("//div/@data-click").extract():
            if "rsv_re_ename" in json_str and "rsv_re_uri" in json_str:
                data = json.loads(json_str.replace("'", '"'))
                print "\t" + data["rsv_re_ename"].encode("gb18030") + "\t" + data["rsv_re_uri"].encode("gb18030"),
        print

    def is_valid_url(self, url):
        if url.startswith("javascript:") or url.startswith("mailto:") or url == "#":
            return False
        filename = url.split("?")[0].split("/")[-1]
        if filename:
            ctype = filename.split(".")[-1].lower()
        else:
            ctype = None
        if ctype in ["jpeg", "jpg", "swf", "rar", "zip", "gz", "gif", "mov", "png", "bmp", "exe", "pps", "db", "txt",
                     "pptx", 'xls', "ppt", "xlsx", "pdf", "tz"]:
            return False
        return True

    def spider_idle(self, spider):

        if spider == self:
            return False
        return True
