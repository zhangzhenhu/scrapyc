import scrapy
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc

from scrapy import signals
from robot.items import NimeiItem
from scrapy.utils.misc import load_object
from scrapyc.server.utils.url import get_url_site,get_url_scheme
import json
import random

class RobotSpider(scrapy.Spider):
    name = "robot"
    allowed_domains = []
    start_urls = [    ]

    def __init__(self,*args, **kwargs):
        super(RobotSpider, self).__init__(*args, **kwargs)
        self._kwargs = kwargs



    def start_requests(self):


        fname = self.settings.get("INPUT_FILE",None)
        if fname:
            with open(fname) as fh:
                for line in fh.readlines():
                    url = line.strip().split()[0]
                    req =  scrapy.Request(url,callback=self.parse)
                    yield req
        url = self.settings.get("url",None)
        if url:
            yield scrapy.Request(url,callback=self.parse)
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
            self.log(response.headers,level=scrapy.log.INFO)
            return
        
        site = get_url_site(response.url)
        print response.url,response.status
        base_url  = get_base_url(response)
        for sel in response.xpath('//a/@href'):
            relative_url = sel.extract()

            abs_url =urljoin_rfc(base_url,relative_url)
            #print abs_url
            schema = get_url_scheme(abs_url)
            if schema not in ["http","https"]:
                continue            
            site = get_url_site(abs_url)
            #yield NimeiItem(url=abs_url,furl=response.url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
            # if site != base_site and site not in ALLOW_SITES:
            #     continue
            # if relative_url.startswith("forum_") or relative_url.startswith("/archives/"):
            #     yield scrapy.Request(abs_url,callback=self.parse)


    def baidu_rpc_request(self,data,furl=""):
        data_post = json.dumps({"url":data})
        server_list = self.settings.get("BAIDU_RPC_SERVER_URL",None)
        if server_list == None:
            self.log("Baidu_RPC no_server",level=scrapy.log.CRITICAL)
            return
        server_url = server_list[random.randint(0, len(server_list)-1)]

        return scrapy.Request(url=server_url,callback=self.baidu_rpc_response,method="POST",body=data_post,headers={"Content-Type":'application/json'},meta={"baidu_rpc":data,"furl":furl})
    
    def baidu_rpc_response(self,response):

        if response.status / 100 != 2:
            self.log("Baidu_RPC %s http_error http_code:%d"%(response.url,response.status),level=scrapy.log.CRITICAL)
            return
        res = json.loads(response.body)
        if res["err_no"] != 0:
            self.log("Baidu_RPC %s rpc_error rpc_code:%d %s"%(response.url,res["err_no"],response.meta["baidu_rpc"]["url"]),level=scrapy.log.CRITICAL)
        else:
            self.log("Baidu_RPC %s %s ok"%(response.meta["furl"],response.meta["baidu_rpc"]["url"]),level=scrapy.log.INFO)

    def is_valid_url(self,url):
        if url.startswith("javascript:") or url.startswith("mailto:") or url =="#":
            return False
        filename = url.split("?")[0].split("/")[-1]
        if filename :
            ctype  = filename.split(".")[-1].lower() 
        else:
            ctype = None
        if ctype in ["jpeg","jpg","swf","rar","zip","gz","gif","mov","png","bmp","exe","pps","db","txt","pptx",'xls',"ppt","xlsx"]:
            return False
        return True


    def spider_idle(self,spider):

        if spider==self:
            return False
        return True
