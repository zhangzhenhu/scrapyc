import scrapy
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc

from scrapy import signals
from robot.items import NimeiItem
from scrapy.utils.misc import load_object
from scrapyc.server.utils.url import get_url_site,get_url_scheme
import json


class RobotSpider(scrapy.Spider):
    name = "robot"
    allowed_domains = []
    start_urls = [    ]

    def __init__(self,*args, **kwargs):
        super(RobotSpider, self).__init__(*args, **kwargs)
        self._kwargs = kwargs



    def start_requests(self):

        # coms = self.settings.get("SITE_SPIDERS")
        # for key,module in coms.items():
        #     comcls = load_object(module)
        #     self.parses[key]= comcls(self)
        #     for item in self.parses[key].start_requests():
        #         yield item
        #self.crawler.signals.connect(self.spider_idle,signals.spider_idle)
        fname = self.settings.get("INPUT_FILE",None)
        if fname:
            with open(fname) as fh:
                for line in fh.readlines():
                    url = line.strip().split()[0]
                    req =  scrapy.Request(url,callback=self.parse)
                    yield req
        for url in self.start_urls:
            req =  scrapy.Request(url,callback=self.parse)
            #req.meta["depth"] =  1
            yield req
        for item in super(RobotSpider, self).start_requests():
            yield item

    def parse(self, response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        
        site = get_url_site(response.url)

        if site in self.parses:
            parser = self.parses[site]
            #self.log("Parser %s %s"%(response.url,parser.name),level=scrapy.log.INFO)
            for item in parser.parse(response) :
                yield item
            return

        base_url  = get_base_url(response)
        for sel in response.xpath('//a/@href'):
            relative_url = sel.extract()

            abs_url =urljoin_rfc(base_url,relative_url)
            #print abs_url
            schema = get_url_scheme(abs_url)
            if schema not in ["http","https"]:
                continue            
            site = get_url_site(abs_url)
            yield NimeiItem(url=abs_url,furl=response.url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":4})
            # if site != base_site and site not in ALLOW_SITES:
            #     continue
            # if relative_url.startswith("forum_") or relative_url.startswith("/archives/"):
            #     yield scrapy.Request(abs_url,callback=self.parse)


    def baidu_rpc_request(self,data):
        data_post = json.dumps({"url":data})
        return scrapy.Request(url=self.settings.get("BAIDU_RPC_SERVER_URL",None),callback=self.baidu_rpc_response,method="POST",body=data_post,headers={"Content-Type":'application/json'})
    
    def baidu_rpc_response(self,response):

        if response.status / 100 != 2:
            self.log("BAIDU_RPC %s http_error http_code:%d"%(response.url,response.status),level=scrapy.log.FATAL)
            return
        res = json.loads(response.body)
        if res["err_no"] != 0:
            self.log("BAIDU_RPC %s rpc_error rpc_code:%d"%(response.url,res["err_no"]),level=scrapy.log.FATAL)



    def spider_idle(self,spider):

        if spider==self:
            return False
        return True
