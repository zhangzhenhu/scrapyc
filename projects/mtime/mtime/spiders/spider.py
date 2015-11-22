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
import happybase
from mtime.items import KeyNameItem
import logging
import re


class MtimeSpider(scrapy.Spider):
    name = "mtime"
    allowed_domains = ["mtime.com"]
    start_urls = []

    # start_urls = [
    #     "http://people.mtime.com/1839529/details.html",
    # ]

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
        self.hbase_conn = happybase.Connection('localhost', autoconnect=True)
        # conn.create_table('mtime_people',{"Detail":{},"ShortComment":{},"LongComment":{}})
        # conn.create_table('mtime_movie',{"Detail":{},"Actor":{},"Director":{},"Writer":{},"Plots":{},"LongComment":{},"ShortComment":{}})
        self.hbase_table_people = self.hbase_conn.table('mtime_people')
        self.hbase_table_movie = self.hbase_conn.table('mtime_movie')
        # self.crawler.signals.connect(self.spider_idle,signals.spider_idle)
        self.DATA_ENCODING = "utf8"
        self.pattern_movie = re.compile("http://movie\.mtime\.com/\d+/$")
        pass

    def start_requests(self):

        flag = False
        for item in super(MtimeSpider, self).start_requests():
            yield item
            flag = True
        if flag:
            return
        yield scrapy.Request("http://people.mtime.com/1839529/details.html", callback=self.parse_person_detail)
        yield scrapy.Request("http://people.mtime.com/1249959/details.html", callback=self.parse_person_detail)
        yield scrapy.Request("http://people.mtime.com/1253921/details.html", callback=self.parse_person_detail)
        yield scrapy.Request("http://people.mtime.com/1839529/filmographies/", callback=self.parse_person_filmographies)
        yield scrapy.Request("http://people.mtime.com/1249009/comment.html", callback=self.parse_person_comment)
        yield scrapy.Request("http://movie.mtime.com/174305/fullcredits.html", callback=self.parse_movie_fullcredits)
        yield scrapy.Request("http://movie.mtime.com/195899/reviews/short/new.html", callback=self.parse_movie_shortcomment)

    def get_key(self, url):
        return "/".join(url.split("/")[:4])+"/"

    def parse_person_detail(self, response):

        self.log("Crawled %s %d" % (response.url, response.status), level=scrapy.log.INFO)
        if response.status / 100 != 2:
            yield scrapy.Request(url=response.url, callback=self.parse_detail)
            return

        # base_url = get_base_url(response)
        detail_data = {}
        row_key = self.get_key(response.url)
        name_cn = response.xpath("//div[@class='per_header']/h2/a/text()").extract()
        name_en = response.xpath("//div[@class='per_header']/p/a/text()").extract()
        if not name_cn and not name_en:
            self.log("Parse_detail %s error %s" % (response.url, response.request.url), level=logging.WARNING)
            return
        if name_cn:
            name_cn = name_cn[0]
        else:
            name_cn = ""
        if name_en:
            name_en = name_en[0]
        else:
            name_en = ""
        name_cn = name_cn.encode(self.DATA_ENCODING)
        name_en = name_en.encode(self.DATA_ENCODING)
        yield KeyNameItem(key=row_key, name_cn=name_cn, name_en=name_en)
        detail_data["Detail:name_cn"] = name_cn
        detail_data["Detail:name_en"] = name_en
        self.log("Parse_detail %s %s" % (response.url, name_cn), level=scrapy.log.INFO)
        # birthday, height, weight, constellation, blood_group = \
        # 提取个人信息
        name_list = response.xpath("//dl[@class='per_info_cont']//strong/text()").extract()
        cur_name = None
        value = []
        for text in response.xpath("//dl[@class='per_info_cont']//text()").extract():
            text = text.strip()
            if not text:
                continue
            if text in name_list:
                if cur_name is None:
                    cur_name = text
                    continue
                name = cur_name.replace(u"：", "").encode(self.DATA_ENCODING)
                value = (u"\t".join(value)).encode(self.DATA_ENCODING)
                detail_data["Detail:" + name] = value
                cur_name = text
                value = []
            else:
                value.append(text)
                # detail_data["detail:" + name] = value
        if cur_name and value:
            name = cur_name.replace(u"：", "").encode(self.DATA_ENCODING)
            value = (u"\t".join(value)).encode(self.DATA_ENCODING)
            detail_data["Detail:" + name] = value

        # for k, v in detail_data.iteritems():
        #     print k, '\t', v

        # # 教育背景
        # edu = response.xpath("//dl[@class='per_info_cont']/dd/text()")
        # if len(edu):
        #     edu_background = edu.extract()[0]
        #     detail_data['detail:edu_background'] = edu_background.encode(self.DATA_ENCODING)
        # 个人传记
        biography = response.xpath("//div[@id='lblPartGraphy']/p/text()")
        if len(biography):
            biography = biography.extract()[0]
            detail_data['Detail:biography'] = biography.encode(self.DATA_ENCODING)

        func_table = {
            "details.html": self.parse_person_detail,
            "filmographies": self.parse_person_filmographies,
            "comment.html": self.parse_person_comment,

        }
        for href in response.xpath('//dl[@id="personNavigationRegion"]/dd/a/@href').extract():
            cat = href.split('/')
            suffix = cat.pop()
            while not suffix and cat:
                suffix = cat.pop()
            if suffix in func_table:
                yield scrapy.Request(href, callback=func_table[suffix])

                # index_url = response.url.replace("/details.html", '')

        self.hbase_table_people.put(row_key, detail_data)
        # for other_url in response.xpath("//dl[@class='per_relalist']/dd/a/@href").extract():
        #     yield scrapy.Request(other_url+"details.html", callback=self.parse_person_detail)

    def parse_person_filmographies(self, response):
        return
        self.log("Crawled %s %d" % (response.url, response.status), level=scrapy.log.INFO)
        if response.status / 100 != 2:
            yield scrapy.Request(url=response.url, callback=self.parse_detail)
            return

        for href in response.xpath("//h3/a/@href").extract():
            if self.pattern_movie.match(href):
                yield scrapy.Request(href, callback=self.parse_movie_detail)

    def parse_person_comment(self, response):
        """
        解析人物的评论
        Args:
            response:

        Returns:

        """
        self.log("Crawled %s %d" % (response.url, response.status), level=scrapy.log.INFO)
        if response.status / 100 != 2:
            yield scrapy.Request(url=response.url, callback=self.parse_detail)
            return
        row_key = self.get_key(response.url)
        detail_data = {}
        for div in response.xpath("//div[@tweetid]"):
            tweetid = div.xpath("@tweetid").extract()
            text = div.xpath("h3/text()").extract()
            if tweetid and text:
                tweetid = tweetid[0].encode(self.DATA_ENCODING)
                text = text[0].encode(self.DATA_ENCODING)
                detail_data["ShortComment:%s" % tweetid] = text
        # for k, v in detail_data.iteritems():
        #     print k, '\t', v
        self.hbase_table_people.put(row_key, detail_data)

        for href in response.xpath('//div[@id="PageNavigator"]/a/@href').extract():
            yield scrapy.Request(href, callback=self.parse_person_comment)

    def parse_movie_detail(self, response):
        """
        解析电影的信息
        Args:
            response:

        Returns:

        """
        self.log("Crawled %s %d" % (response.url, response.status), level=scrapy.log.INFO)
        if response.status / 100 != 2:
            yield scrapy.Request(url=response.url, callback=self.parse_detail)
            return

    def parse_movie_fullcredits(self, response):
        """
        解析电影的演员列表
        Args:
            response:

        Returns:

        """
        self.log("Crawled %s %s %d" % ("parse_movie_fullcredits",response.url, response.status), level=scrapy.log.INFO)
        if response.status / 100 != 2:
            yield scrapy.Request(url=response.url, callback=self.parse_detail)
            return
        row_key = self.get_key(response.url)
        actor_data = {}
        for dd in response.xpath("//div[@class='db_actor']//dd"):
            actor_url = dd.xpath("div[@class='actor_tit']//a/@href").extract()
            character_name = dd.xpath("div[@class='character_tit']//h3/text()").extract()
            if not actor_url:
                continue
            actor_url = actor_url[0].strip()
            if character_name:
                character_name = character_name[0].encode(self.DATA_ENCODING)
            else:
                character_name = ''
            actor_key = self.get_key(actor_url)
            actor_data["Actor:" + actor_key] = character_name
            # print "************************",actor_url + "details.html"
            yield scrapy.Request(actor_url + "details.html", callback=self.parse_person_detail)
        self.hbase_table_movie.put(row_key, actor_data)

        for div in response.xpath("//div[@class='credits_list']"):
            h = div.xpath('h4/text()').extract()[0]
            url = div.xpath('.//a/@href').extract()[0].strip()
            title = div.xpath('.//a[@title]/@title').extract()

            if not title:
                title = div.xpath('.//a/text()').extract()
            title = title[0].encode(self.DATA_ENCODING)
            key = self.get_key(url)
            # title = title.encode(self.DATA_ENCODING)
            if "Director" in h:
                self.hbase_table_movie.put(row_key, {"Director:%s" % key: title})
            elif 'Writer' in h:
                self.hbase_table_movie.put(row_key, {"Writer:%s" % key: title})
            # print "************************",url + "details.html"
            yield scrapy.Request(url + "details.html", callback=self.parse_person_detail)


    def parse_movie_shortcomment(self,response):
        """
        解析电影的微评论
        Args:
            response:

        Returns:

        """
        self.log("Crawled %s %d" % (response.url, response.status), level=scrapy.log.INFO)
        if response.status / 100 != 2:
            yield scrapy.Request(url=response.url, callback=self.parse_detail)
            return
        row_key = self.get_key(response.url)

        comment_data = {}
        for div in response.xpath("//div[@tweetid]"):
            tweetid = div.xpath("@tweetid").extract()
            text = div.xpath("h3/text()").extract()
            if tweetid and text:
                tweetid = tweetid[0].encode(self.DATA_ENCODING)
                text = text[0].encode(self.DATA_ENCODING)
                comment_data["ShortComment:%s" % tweetid] = text
        # for k, v in detail_data.iteritems():
        #     print k, '\t', v
        self.hbase_table_movie.put(row_key, comment_data)

        for href in response.xpath('//div[@id="PageNavigator"]/a/@href').extract():
            yield scrapy.Request(href, callback=self.parse_movie_shortcomment)



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
