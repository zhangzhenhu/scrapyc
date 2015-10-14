import scrapy
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc,url_query_parameter

from scrapy import signals
from robot.items import NimeiItem
from robot.spiders import base
from scrapy.utils.misc import load_object
from scrapyc.server.utils.url import get_url_site,get_url_scheme
import json


class BuluoSpider(base.RobotSpider):
    name = "buluo.qq"
    allowed_domains = []
    start_urls = [    ]
    parses = {}

    def start_requests(self):

        flag = False
        for item in super(BuluoSpider, self).start_requests():
            yield item
            flag = True 
        if flag:
            return
        
        for bid in range(10038,250000):
            url = 'http://buluo.qq.com/cgi-bin/bar/post/get_post_by_page?bid=%s&num=20&start=0&bkn'%(bid)
            refer = "http://buluo.qq.com/p/barindex.html?bid=%s"%bid
            yield scrapy.Request(url=url,headers={"Referer":refer})
            yield self.baidu_rpc_request({"url":refer,"src_id":22})
  


    def parse(self, response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return

        res_data = json.loads(response.body)
        if res_data["retcode"]  != "0" and res_data["retcode"] != 0:
            self.log("Crawled %s %s"%(response.url,res_data["retcode"]),level=scrapy.log.CRITICAL)
            return
        bid = url_query_parameter(response.url,'bid')
        start = url_query_parameter(response.url,'start')
        for item in res_data["result"]["posts"]:
            url = "http://buluo.qq.com/p/detail.html?bid=%s&pid=%s"%(bid,item["pid"])
            yield self.baidu_rpc_request({"url":url,"src_id":22})
        start = int(start)
        
        if int(res_data["result"]["total"]) > start+20:
            next_url = 'http://buluo.qq.com/cgi-bin/bar/post/get_post_by_page?bid=%s&num=20&start=%s&bkn'%(bid,start+20)
            self.log("SendCrawl %s Total:%d"%(next_url,int(res_data["result"]["total"])),level=scrapy.log.INFO)
            yield scrapy.Request(url=next_url,headers={"Referer":"http://buluo.qq.com/p/barindex.html?bid=%s"%bid})






    def spider_idle(self,spider):

        if spider==self:
            return False
        return True
