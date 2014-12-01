# -*- coding: utf-8 -*-
import scrapy
from shixin.items import ShixinItem
import re
from datetime import datetime
from twisted.enterprise import adbapi
import MySQLdb.cursors
class CourtSpider(scrapy.Spider):
    name = "court"
    allowed_domains = ["court.gov.cn"]
    start_urls = (
        'http://shixin.court.gov.cn/personMore.do?currentPage=1',
        'http://shixin.court.gov.cn/unitMore.do?currentPage=1',
    )
    _pattern = re.compile(r'var totalPage = \d+;',re.M)

    def __init__(self,*args,**kwargs):
        
        scrapy.Spider.__init__(self,**kwargs)
        scrapy.log.start()
    def init(self):      
        M_SQLDB_CONF = self.settings.get("M_SQLDB_CONF")
        assert M_SQLDB_CONF, "Please set SQL DATABASE conf in shixin/settings.py ! eg:M_SQLDB_CONF={'host':'localhost','port':3306,'user':'wangpan','passwd':'wangpan','db':'wangpan'}"


        self.sql_conn=MySQLdb.connect(**M_SQLDB_CONF)
        cursor = self.sql_conn.cursor()     
        cursor.execute("select id from shixin;")
        self.have_keys = {}
        for row in cursor.fetchall():
            self.have_keys[int(row[0])] = 0
        self.sql_conn.commit()


    def _sql_connect(self):
        self.sql_conn=MySQLdb.connect(**self._msql_config)


    def start_requests(self):
        self.init()

        return [
            scrapy.Request( 'http://shixin.court.gov.cn/personMore.do?currentPage=1',callback=self.parse_start),
            scrapy.Request( 'http://shixin.court.gov.cn/unitMore.do?currentPage=1',callback=self.parse_start),

        ]


    def parse(self, response):
        pass

    def parse_start(self,response):
        if response.status != 200:
            yield response.request
            return

        url_prefix = response.url[:-1]

        page,count = self._get_page_count(response)
        self.log("from %s get PageCount %d"%(response.url,page))

        for i in range(2,page):
            yield scrapy.Request(url_prefix+str(i),callback=self.parse_index)

        for ret in self.parse_index(response):
            yield ret

    def _get_page_count(self,response):
        #print html
        ret=self._pattern.search(response.body)
        page=ret.group().split("=")[1].replace(';','').strip()
        #print page
        try:    
            ss=re.search(u'\u5171\d+\u6761',response.body.decode("utf8")).group()
            count=re.search(u'\d+',ss).group()
        except Exception,e:
            self.log(str(e),scrapy.log.ERROR)
            count=(int(page)-1) *15
        
        return int(page),int(count)
        #quit()
        try:
            ret=tree.xpath('//input[@id="pagenum"]/../text()')
            item=ret[-1].strip()
            item=item.split()
            total=item[1].split("/")[-1]
            return int(total)
        except Exception,e:
            log(str(e))
        return -1

    def parse_index(self,response):
        #global ID,REPEAT
        if response.status != 200:
            self.log("get %s failed %s ",(response.url,response.status),scrapy.log.WARNING)
            yield response.request
            return

        DETAIL_URL="http://shixin.court.gov.cn/detail?id="
        items=response.xpath("//tr")
        count=0
        for item in items[1:]:
            ids=item.xpath("td/a/@id")
            if not ids:continue
            id=ids[0].extract()
            #num=item.xpath("td/text()")[1]
            #publish=item.xpath("td/text()")[2]
            if int(id) in self.have_keys:
                self.have_keys[int(id)] +=1
                item = ShixinItem()
                item["id"] = id
                item["last_crawl_time"] = datetime.now()                
                continue
            self.log("from %s  get detail id %s"%(response.url,id))

            yield scrapy.Request(DETAIL_URL+id,callback=self.parse_detail)

    def parse_detail(self,response):

            if response.status != 200:
                self.log("get %s failed %s ",(response.url,response.status),scrapy.log.WARNING)
                return response.request 

            item = ShixinItem.from_json(response.body)
            item["last_crawl_time"] = datetime.now()
            return item




