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
    name = "hot.163.com"
    allowed_domains = []
    start_urls = [    ]
    parses = {}

    def start_requests(self):
        yield scrapy.Request("http://hot.163.com/group/list/100/week/grownup/ranking?offset=0",callback=self.parse_rank)
        yield scrapy.Request("http://hot.163.com/group/list/channel/2/100/week/grownup/ranking?offset=0",callback=self.parse_rank)
        yield scrapy.Request("http://hot.163.com/group/list/channel/3/100/week/grownup/ranking?offset=0",callback=self.parse_rank)
        yield scrapy.Request("http://hot.163.com/group/list/channel/4/100/week/grownup/ranking?offset=0",callback=self.parse_rank)
        yield scrapy.Request("http://hot.163.com/group/list/channel/5/100/week/grownup/ranking?offset=0",callback=self.parse_rank)
        yield scrapy.Request("http://hot.163.com/group/list/channel/6/100/week/grownup/ranking?offset=0",callback=self.parse_rank)


        yield scrapy.Request("http://hot.163.com/post/list/3/0/1000/hot",callback=self.parse)
        yield scrapy.Request("http://hot.163.com/post/list/3/0/1000/new",callback=self.parse)
        yield scrapy.Request("http://hot.163.com/operate/PC/activity/recommend",callback=self.parse)
        yield scrapy.Request("http://hot.163.com/operate/PC/official/announcement",callback=self.parse)
        #yield scrapy.Request("http://hot.163.com/post/list/group/1257003701853608/3/0/1000/new",callback=self.parse)

        for item in super(RobotSpider, self).start_requests():
            yield item

    def parse(self, response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        
        res_data = json.loads(response.body)
        if response.url.startswith("http://hot.163.com/post/list/"):
            for item in res_data["data"]:
                url = "http://hot.163.com/group/%s/post/%s/"%(item["groupAlias"],item["id"])
                yield self.baidu_rpc_request({"url":url,"src_id":4})
                yield NimeiItem(url=url,furl=response.url)
                url = "http://hot.163.com/user/%s"%item["creator"]["userId"]
                yield self.baidu_rpc_request({"url":url,"src_id":4})
                yield NimeiItem(url=url,furl=response.url)
                url = "http://hot.163.com/group/%s"%item["groupAlias"]
                yield self.baidu_rpc_request({"url":url,"src_id":4})
                yield NimeiItem(url=url,furl=response.url)
                url = "http://hot.163.com/group/%s/post/%s/#!comment"%(item["groupAlias"],item["id"])
                yield self.baidu_rpc_request({"url":url,"src_id":4})
                yield NimeiItem(url=url,furl=response.url)
                url = "http://hot.163.com/post/list/group/%s/3/0/1000/new"%item["groupId"]
                yield scrapy.Request(url=url)
        elif response.url.startswith("http://hot.163.com/operate/PC/"):
            for item in res_data["data"]:
                yield self.baidu_rpc_request({"url":item["url"],"src_id":4})
                yield NimeiItem(url=item["url"],furl=response.url)
    
    def parse_rank(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return     
        res_data = json.loads(response.body)
        for item in res_data["data"]:
            url = "http://hot.163.com/post/list/group/%s/3/0/1000/new"%item["groupId"]
            yield scrapy.Request(url=url)
            url = "http://hot.163.com/group/%s"%item["alias"]
            yield self.baidu_rpc_request({"url":url,"src_id":4})



    def spider_idle(self,spider):

        if spider==self:
            return False
        return True
