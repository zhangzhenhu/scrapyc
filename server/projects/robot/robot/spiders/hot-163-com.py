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
                url = "http://hot.163.com/post/list/group/%s/3/0/100/new"%item["groupId"]
                yield scrapy.Request(url=url)
        elif response.url.startswith("http://hot.163.com/operate/PC/"):
            for item in res_data["data"]:
                yield self.baidu_rpc_request({"url":item["url"],"src_id":4})
                yield NimeiItem(url=item["url"],furl=response.url)

    def spider_idle(self,spider):

        if spider==self:
            return False
        return True
