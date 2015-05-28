from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc

from scrapy import signals
from robot.items import NimeiItem
import scrapy

class Parser(object):
    """docstring for Parser"""
    def __init__(self, spider):
        super(Parser, self).__init__()
        self.spider = spider
    def start_requests():
        headers = {
            "Content-Type":"application/x-www-form-urlencoded",
            "X-Requested-With":"XMLHttpRequest",
        }
        url = "www.weihai.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=%d&endrecord=%d&perpage=100" %(1,100)
        yield scrapy.Request(url,method="POST",body="appid=1&webid=1&path=%2F&columnid=562&sourceContentType=1&unitid=2565&webname=%E5%A8%81%E6%B5%B7%E5%B8%82%E6%94%BF%E5%BA%9C%E9%97%A8%E6%88%B7%E7%BD%91%E7%AB%99&permissiontype=0",headers = headers)
        for i in range(1,5000):
            url = "www.weihai.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=%d&endrecord=%d&perpage=100" %(i*100,i*100+100)

            yield scrapy.Request(url,method="POST",body="appid=1&webid=1&path=%2F&columnid=562&sourceContentType=1&unitid=2565&webname=%E5%A8%81%E6%B5%B7%E5%B8%82%E6%94%BF%E5%BA%9C%E9%97%A8%E6%88%B7%E7%BD%91%E7%AB%99&permissiontype=0",headers = headers)
        pass
    def parse(self,response):


        base_url  = get_base_url(response)
        for sel in response.xpath('//a/@href')[1:]:
            relative_url = sel.extract()
            abs_url =urljoin_rfc(base_url,relative_url)
            yield NimeiItem(url=abs_url,furl=response.url)    


            