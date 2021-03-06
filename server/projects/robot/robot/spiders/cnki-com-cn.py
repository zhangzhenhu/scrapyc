# encoding=utf8
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc

from scrapy import signals
from robot.items import NimeiItem
from robot.spiders import base
import scrapy
from scrapyc.server.utils.url import get_url_site, get_url_scheme
import urlparse
import re
import datetime


class WwwSpider(base.RobotSpider):
    name = "www.cnki.com.cn"

    allowed_domains = []
    start_urls = []

    def start_requests(self):
        yield scrapy.Request("http://www.cnki.com.cn/CJFD/CJFD_index.htm")

        for item in super(WwwSpider, self).start_requests():
            yield item
            # PATTERN1=re.compile(".*thread\-\d+\-\d+\-\d+\.html.*")

    def parse(self, response):
        self.log("Crawled %s %d" % (response.url, response.status), level=scrapy.log.INFO)
        # self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            yield scrapy.Request(url=response.url)
            return
        base_url = get_base_url(response)
        # 解析文章
        for href in response.xpath("//table[@id='articleList']/tr/td/a/@href").extract():
            relative_url = href
            abs_url = urljoin_rfc(base_url, relative_url)
            yield self.baidu_rpc_request({"url": abs_url, "src_id": 22}, furl=response.url)

        # 解析当年各期
        # 只更新最近2期的，为的是减少数据量，提高更新频次
        for href in response.xpath("//table[@id='issueList']/tr/td/a/@href").extract()[-2:]:#最后两条
            relative_url = href
            abs_url = urljoin_rfc(base_url, relative_url)
            # yield self.baidu_rpc_request({"url":abs_url,"src_id":22})
            yield scrapy.Request(url=abs_url)
            self.log("Parse %s %s " % (response.url, abs_url), level=scrapy.log.INFO)


            # 解析历年各期
            # for href in response.xpath("//table[@id='yearList']//a/@href").extract():

            #    relative_url = href
            #    abs_url =urljoin_rfc(base_url,relative_url)
            #    yield self.baidu_rpc_request({"url":abs_url,"src_id":22})
            #    yield scrapy.Request(url=abs_url)

        # 解析期刊首页
        for href in response.xpath("//table[@class='r_list']/tr/td/span/span[1]/a/@href").extract():
            relative_url = href
            abs_url = urljoin_rfc(base_url, relative_url)
            # yield self.baidu_rpc_request({"url":abs_url,"src_id":22})
            yield scrapy.Request(url=abs_url)


            # if "Journal" in relative_url or 'Navi' in relative_url:

            #     yield scrapy.Request(url=abs_url)
            #     self.log("Parse %s %s"%(response.url,abs_url),level=scrapy.log.INFO) 
            # elif "/Article/" in relative_url:
            #     #abs_url =urljoin_rfc(base_url,relative_url)
            #     #yield self.baidu_rpc_request({"url":abs_url,"src_id":4})
            #     self.log("Parse %s %s"%(response.url,abs_url),level=scrapy.log.INFO)                


class CDmdSpider(base.RobotSpider):
    name = "cdmd.cnki.com.cn"

    allowed_domains = []
    start_urls = []

    def start_requests(self):
        for i in range(1, 42):
            yield scrapy.Request("http://cdmd.cnki.com.cn/Area/CDMDUnit-%04d.htm" % i, callback=self.parse_unit)

        for item in super(CDmdSpider, self).start_requests():
            yield item
            # PATTERN1=re.compile(".*thread\-\d+\-\d+\-\d+\.html.*")

    def parse_unit(self, response):
        self.log("Crawled %s %d" % (response.url, response.status), level=scrapy.log.INFO)
        # self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        site = get_url_site(response.url)
        base_url = get_base_url(response)

        for href in response.xpath("//a[@class='zt_name']/@href").extract():
            # if not self.is_valid_url(href):
            #     continue
            if href == "#": continue
            relative_url = href
            abs_url = urljoin_rfc(base_url, relative_url)
            yield self.baidu_rpc_request({"url": abs_url, "src_id": 4}, furl=response.url)
            yield scrapy.Request(url=abs_url, callback=self.parse_cdmd)

    def parse_cdmd(self, response):
        self.log("Crawled %s %d" % (response.url, response.status), level=scrapy.log.INFO)
        # self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return

        base_url = get_base_url(response)
        # 解析期刊
        count = 0
        for href in response.xpath("//a[@class='zt_name']/@href").extract():
            if not self.is_valid_url(href):
                continue
            relative_url = href
            abs_url = urljoin_rfc(base_url, relative_url)
            yield self.baidu_rpc_request({"url": abs_url, "src_id": 22}, furl=response.url)
            count += 1



        # 预测后续翻页
        if count in [15, 21] and re.search("/Area/CDMDUnitArticle-\d+-\d{4}-\d+\.htm", response.url):
            up = response.url.split("-")
            pageNo = up[-1].split('.')[0]
            pageNo = int(pageNo) + 1
            if pageNo < 150:
                abs_url = up[0] + "-" + up[1] + "-" + up[2] + "-" + str(pageNo) + ".htm"
                yield self.baidu_rpc_request({"url": abs_url, "src_id": 22}, furl=response.url)
                yield scrapy.Request(url=abs_url, callback=self.parse_cdmd)
                self.log("Nimei %s" % abs_url, level=scrapy.log.INFO)

        # 解析历年索引页
        # for href in response.xpath("//a[@class='content_gray02']/@href").extract():
        #     relative_url = href
        #     abs_url =urljoin_rfc(base_url,relative_url)
        #     yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
        #     yield scrapy.Request(url=abs_url,callback=self.parse_cdmd)

        # 解析当前索引页的翻页
        js = response.xpath("//table/tbody/tr/td/script").extract()
        if js:
            js = js[0]
            articleTotal = re.search("var\s+articleTotal\s+=\s+(\d+);", js)
            countPerPage = re.search("var\s+countPerPage\s+=\s+(\d+);", js)
            curYear = re.search("var\s+curYear\s+=\s+(\d+);", js)
            curUnit = re.search("var\s+curUnit\s+=\s+(\d+);", js)
            if articleTotal and curUnit and countPerPage and curYear:
                articleTotal = int(articleTotal.groups()[0])
                countPerPage = int(countPerPage.groups()[0])
                curYear = curYear.groups()[0]
                curUnit = curUnit.groups()[0]
                totalPage = articleTotal / countPerPage
                if articleTotal % countPerPage != 0:
                    totalPage += 1
                i = 1
                # print response.url,url,articleTotal,countPerPage,totalPage
                while i <= totalPage:
                    url = "http://cdmd.cnki.com.cn/Area/CDMDUnitArticle-%s-%s-%d.htm" % (curUnit, curYear, i)
                    # print response.url,url,articleTotal,countPerPage,totalPage
                    self.log("Nimei-js %s" % url, level=scrapy.log.INFO)
                    yield scrapy.Request(url=url, callback=self.parse_cdmd)
                    i += 1


class CPfdSpider(base.RobotSpider):
    name = "cpfd.cnki.com.cn"

    allowed_domains = []
    start_urls = []

    def start_requests(self):

        for i in range(1, 32):
            yield scrapy.Request("http://cpfd.cnki.com.cn/Area/CPFDUnit-%04d.htm" % i, callback=self.parse_unit)
        # yield scrapy.Request("")
        for item in super(CPfdSpider, self).start_requests():
            yield item

    def parse_unit(self, response):
        self.log("Crawled %s %d" % (response.url, response.status), level=scrapy.log.INFO)
        # self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        site = get_url_site(response.url)
        base_url = get_base_url(response)

        for href in response.xpath("//a[@class='zt_name']/@href").extract():
            # if not self.is_valid_url(href):
            #     continue
            if href == "#": continue
            relative_url = href
            abs_url = urljoin_rfc(base_url, relative_url)
            yield self.baidu_rpc_request({"url": abs_url, "src_id": 22}, furl=response.url)
            yield scrapy.Request(url=abs_url, callback=self.parse_cdmd)

    def parse_cdmd(self, response):
        self.log("Crawled %s %d" % (response.url, response.status), level=scrapy.log.INFO)
        # self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        base_url = get_base_url(response)
        # 解析期刊
        count = 0
        for href in response.xpath("//a[@class='zt_name']/@href").extract():
            if not self.is_valid_url(href):
                continue
            relative_url = href
            abs_url = urljoin_rfc(base_url, relative_url)
            yield self.baidu_rpc_request({"url": abs_url, "src_id": 22}, furl=response.url)
            if "CPFDCONFArticleList" in relative_url:
                yield scrapy.Request(url=abs_url, callback=self.parse_cdmd)
            count += 1


        # 预测后续翻页
        if count in [15, 21] and re.search("/Area/CPFDCONFArticleList-[\d\w]+-\d+\.htm", response.url):
            up = response.url.split("-")
            pageNo = up[-1].split('.')[0]
            pageNo = int(pageNo) + 1
            if pageNo < 150:
                abs_url = up[0] + "-" + up[1] + "-" + str(pageNo) + ".htm"
                yield self.baidu_rpc_request({"url": abs_url, "src_id": 22}, furl=response.url)
                yield scrapy.Request(url=abs_url, callback=self.parse_cdmd)
                self.log("Nimei %s" % abs_url, level=scrapy.log.INFO)


        # 解析历年索引页
        for href in response.xpath("//a[@class='content_gray02']/@href").extract():
            relative_url = href
            abs_url = urljoin_rfc(base_url, relative_url)
            yield self.baidu_rpc_request({"url": abs_url, "src_id": 22}, furl=response.url)
            yield scrapy.Request(url=abs_url, callback=self.parse_cdmd)

        # 解析当前索引页的翻页
        js = response.xpath("//table/tr/td/script").extract()
        if js:
            js = js[0]
            articleTotal = re.search("var\s+articleTotal\s+=\s+(\d+);", js)
            countPerPage = re.search("var\s+countPerPage\s+=\s+(\d+);", js)
            curCode = re.search("var\s+curCode\s+=\s+'([\w\d]+)';", js)
            # curPage  = re.search("var\s+curPage \s+=\s+(\d+);",js)
            if articleTotal and curCode:
                articleTotal = int(articleTotal.groups()[0])
                countPerPage = int(countPerPage.groups()[0])
                curCode = curCode.groups()[0]
                # curPage = curPage.groups()[0]
                totalPage = articleTotal / countPerPage
                if articleTotal % countPerPage != 0:
                    totalPage += 1
                i = 1
                # print response.url,url,articleTotal,countPerPage,totalPage
                while i <= totalPage:
                    url = "http://cpfd.cnki.com.cn/Area/CPFDCONFArticleList-%s-%d.htm" % (curCode, i)
                    self.log("Nimei-js %s" % url, level=scrapy.log.INFO)
                    yield scrapy.Request(url=url, callback=self.parse_cdmd)
                    i += 1


class EpubSpider(base.RobotSpider):
    name = "epub.cnki.net"

    allowed_domains = []
    start_urls = []

    def start_requests(self):

        for i in range(1, 460):
            yield scrapy.Request(
                "http://epub.cnki.net/kns/Navi/brief.aspx?curpage=%d&RecordsPerPage=50&QueryID=14&ID=&turnpage=1&tpagemode=L&dbPrefix=34_CATALOG&Fields=&DisplayMode=listmode&pagename=ASP.navi_cdmdcatalog_aspx&NaviID=34&sKuaKuID=14" % i,
                callback=self.parse_unit)
        # yield scrapy.Request("")
        for item in super(EpubSpider, self).start_requests():
            yield item

    def parse_unit(self, response):
        self.log("Crawled %s %d" % (response.url, response.status), level=scrapy.log.INFO)
        # self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        site = get_url_site(response.url)
        base_url = get_base_url(response)

        for href in response.xpath("//a[@class='zt_name']/@href").extract():
            # if not self.is_valid_url(href):
            #     continue
            if href == "#": continue
            relative_url = href
            abs_url = urljoin_rfc(base_url, relative_url)
            yield self.baidu_rpc_request({"url": abs_url, "src_id": 22}, furl=response.url)
            yield scrapy.Request(url=abs_url, callback=self.parse_cdmd)

    def parse_cdmd(self, response):
        self.log("Crawled %s %d" % (response.url, response.status), level=scrapy.log.INFO)
        # self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        base_url = get_base_url(response)
        # 解析期刊
        count = 0
        for href in response.xpath("//a[@class='zt_name']/@href").extract():
            if not self.is_valid_url(href):
                continue
            relative_url = href
            abs_url = urljoin_rfc(base_url, relative_url)
            yield self.baidu_rpc_request({"url": abs_url, "src_id": 22}, furl=response.url)
            if "CPFDCONFArticleList" in relative_url:
                yield scrapy.Request(url=abs_url, callback=self.parse_cdmd)
            count += 1


        # 预测后续翻页
        if count in [15, 21] and re.search("/Area/CPFDCONFArticleList-[\d\w]+-\d+\.htm", response.url):
            up = response.url.split("-")
            pageNo = up[-1].split('.')[0]
            pageNo = int(pageNo) + 1
            if pageNo < 150:
                abs_url = up[0] + "-" + up[1] + "-" + str(pageNo) + ".htm"
                yield self.baidu_rpc_request({"url": abs_url, "src_id": 4}, furl=response.url)
                yield scrapy.Request(url=abs_url, callback=self.parse_cdmd)
                self.log("Nimei %s" % abs_url, level=scrapy.log.INFO)


        # 解析历年索引页
        # for href in response.xpath("//a[@class='content_gray02']/@href").extract():
        #     relative_url = href
        #     abs_url =urljoin_rfc(base_url,relative_url)
        #     yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
        #     yield scrapy.Request(url=abs_url,callback=self.parse_cdmd)

        # 解析当前索引页的翻页
        js = response.xpath("//table/tr/td/script").extract()
        if js:
            js = js[0]
            articleTotal = re.search("var\s+articleTotal\s+=\s+(\d+);", js)
            countPerPage = re.search("var\s+countPerPage\s+=\s+(\d+);", js)
            curCode = re.search("var\s+curCode\s+=\s+'([\w\d]+)';", js)
            # curPage  = re.search("var\s+curPage \s+=\s+(\d+);",js)
            if articleTotal and curCode:
                articleTotal = int(articleTotal.groups()[0])
                countPerPage = int(countPerPage.groups()[0])
                curCode = curCode.groups()[0]
                # curPage = curPage.groups()[0]
                totalPage = articleTotal / countPerPage
                if articleTotal % countPerPage != 0:
                    totalPage += 1
                i = 1
                # print response.url,url,articleTotal,countPerPage,totalPage
                while i <= totalPage:
                    url = "http://cpfd.cnki.com.cn/Area/CPFDCONFArticleList-%s-%d.htm" % (curCode, i)
                    self.log("Nimei-js %s" % url, level=scrapy.log.INFO)
                    yield scrapy.Request(url=url, callback=self.parse_cdmd)
                    i += 1
