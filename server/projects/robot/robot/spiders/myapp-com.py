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
    name = "android.myapp.com"
    allowed_domains = []
    start_urls = [    ]
    parses = {}

    def start_requests(self):

        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=0&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=-10&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=103&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=101&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=122&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=102&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=112&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=106&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=104&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=110&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=115&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=119&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=111&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=107&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=118&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=108&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=100&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=114&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=117&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=109&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=105&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=113&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=116&pageSize=100&pageContext=0",callback=self.parse)


        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=2&categoryId=147&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=2&categoryId=121&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=2&categoryId=144&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=2&categoryId=148&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=2&categoryId=149&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=2&categoryId=153&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=2&categoryId=146&pageSize=100&pageContext=0",callback=self.parse)
        yield scrapy.Request("http://android.myapp.com/myapp/cate/appList.htm?orgame=2&categoryId=151&pageSize=100&pageContext=0",callback=self.parse)

        for item in super(RobotSpider, self).start_requests():
            yield item

    def parse(self, response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        
        res_data = json.loads(response.body)
        for item in res_data["obj"]:
            url = "http://android.myapp.com/myapp/detail.htm?apkName=%s"%(item["pkgName"])
            yield self.baidu_rpc_request({"url":url,"src_id":4})
            yield NimeiItem(url=url,furl=response.url)
        if res_data["count"] ==100:
            url = response.url
            hehe = url.split("=")
            hehe[-1] = str(int(hehe[-1])+100)
            url = "=".join(hehe)
            yield scrapy.Request(url)




    def spider_idle(self,spider):

        if spider==self:
            return False
        return True
