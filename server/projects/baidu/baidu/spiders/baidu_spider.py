import scrapy
from baidu.items import BaiduUserItem,BaiduShareItem,BaiduFileItem
import datetime
import time
from baidu import settings
import re
from twisted.enterprise import adbapi
import MySQLdb.cursors
import urlparse
import json
from scrapy import log
#from scrapy.conf import settings


class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = [ ]
    start_urls = []
    
    def __init__(self,*args, **kwargs):
        super(BaiduSpider, self).__init__(*args, **kwargs)
        self._kwargs = kwargs

    def init_from_cmdline(self):
        
        #self.log(str(kwargs),level=log.INFO)
        print "[-------fuck-------]",self._kwargs

        if "M_BAIDU_USER_LIST" in self._kwargs:
            self.M_BAIDU_USER_LIST= self._kwargs["M_BAIDU_USER_LIST"]
        else:
            self.M_BAIDU_USER_LIST = None
        if "M_SOURCE" in self._kwargs:
            self.M_SOURCE = self._kwargs["M_SOURCE"]
        else:
            self.M_SOURCE = None
        if "M_BAIDU_SQL_USER" in self._kwargs:
            self.M_BAIDU_SQL_USER = self._kwargs["M_BAIDU_SQL_USER"]
        else:
            self.M_BAIDU_SQL_USER = None

        if "M_ACTION" in self._kwargs:
            self.M_ACTIONS = self._kwargs["M_ACTION"]
        else:
            self.M_ACTIONS = None

    def requestUserInfo(self,uk):
        return scrapy.Request('http://pan.baidu.com/pcloud/user/getinfo?query_uk=%d&t=%d&channel=chunlei&clienttype=0&web=1'%(uk,int(time.time())),
                                           callback=self.parseUserInfo)
    def requestUserFanList(self,uk,start=0):
        return scrapy.Request('http://pan.baidu.com/pcloud/friend/getfanslist?query_uk=%d&limit=24&start=%d&channel=chunlei&clienttype=0&web=1'%(uk,start),
                callback=self.parseUserFanList)
    
    def requestUserFollowList(self,uk,start=0):
        return scrapy.Request('http://pan.baidu.com/pcloud/friend/getfollowlist?query_uk=%d&limit=24&start=%d&channel=chunlei&clienttype=0&web=1'%(uk,start),
                                          callback=self.parseUserFollowList)
    
    def reqeusetUserShareList(self,uk,start=0):
        return scrapy.Request('http://pan.baidu.com/pcloud/feed/getsharelist?category=0&auth_type=1&request_location=share_home&start=%d&limit=100&query_uk=%d'%(start,uk),
                                           callback=self.parseShareList)
    
    def start_requests(self):

        self.init_from_cmdline()
        
        M_SQLDB_CONF = self.settings.get("M_SQLDB_CONF")
        assert M_SQLDB_CONF, "Please set SQL DATABASE conf in baidu/settings.py ! eg:M_SQLDB_CONF={'host':'localhost','port':3306,'user':'wangpan','passwd':'wangpan','db':'wangpan'}"
        self._msql_config=M_SQLDB_CONF
        self._sql_connect()

        #self.sql_conn=MySQLdb.connect(**M_SQLDB_CONF) 
        #self.sql_cursor = self.sql_conn.cursor()

        if not self.M_SOURCE:
            self.M_SOURCE = self.settings.get("M_SOURCE")
        #M_BAIDU_SQL_USER=None
        #M_BAIDU_USER_LIST=None
        
        self.log("[M_SOURCE] %s "%self.M_SOURCE)
        if "db" in self.M_SOURCE:
            if not self.M_BAIDU_SQL_USER:
                self.M_BAIDU_SQL_USER = self.settings.get("M_BAIDU_SQL_USER")
            self.log("[M_BAIDU_SQL_USER] %s" %self.M_BAIDU_SQL_USER,level=log.INFO)
        if "manual" in self.M_SOURCE:
            if not self.M_BAIDU_USER_LIST:
                self.M_BAIDU_USER_LIST = self.settings.get("M_BAIDU_USER_LIST")
            self.log("[M_BAIDU_USER_LIST] %s" %self.M_BAIDU_USER_LIST,level=log.INFO)
            
            if  type(self.M_BAIDU_USER_LIST) != list:
                self.M_BAIDU_USER_LIST = self.M_BAIDU_USER_LIST.strip().split()
            
                
        
        #self._sql_str="select uk from baidu_user;"
        self.uk_list=[]
       
        if self.M_BAIDU_USER_LIST :
            self.uk_list += self.M_BAIDU_USER_LIST
        elif self.M_BAIDU_SQL_USER:        
            cursor = self.sql_conn.cursor()     
            cursor.execute(self.M_BAIDU_SQL_USER)
            for row in cursor.fetchall():
                self.uk_list.append( row[0])
            self.sql_conn.commit()
                
        requests=[]
        if not self.M_ACTIONS:
            self.M_ACTIONS=self.settings.get("M_ACTION",["userInfo"])
        
    
        self.log("[M_ACTION] %s"%(self.M_ACTIONS),level=log.INFO)
        self.log("select total %d uk"%len(self.uk_list),level=log.INFO)
        for uk in self.uk_list:
            if not uk:continue
            uk=int(uk)
            if "userShare" in self.M_ACTIONS:
                requests.append(self.reqeusetUserShareList(uk))

            if "userInfo" in self.M_ACTIONS:
                requests.append(self.requestUserInfo(uk))
            if "userFollow" in self.M_ACTIONS:
                requests.append(self.requestUserFanList(uk))
                requests.append(self.requestUserFollowList(uk)) 
        return requests

    def _sql_connect(self):
        self.sql_conn=MySQLdb.connect(**self._msql_config)

    def _setInvalid(self,uk,value,condition):
        sql_share="UPDATE baidu_share SET is_valid=%d where uk=%d and is_valid=%d "%(value,uk,condition)
        sql_file="UPDATE baidu_file SET is_valid=%d where uk=%d and is_valid=%d"%(value,uk,condition)
        try:            
            cursor = self.sql_conn.cursor()  
            cursor.execute(sql_share)
            cursor.execute(sql_file)
            self.sql_conn.commit()
        except (AttributeError, MySQLdb.OperationalError):  
            self._sql_connect()  
            cursor = self.sql_conn.cursor()  
            cursor.execute(sql_share)
            cursor.execute(sql_file)
            self.sql_conn.commit()   


    def parseShareList(self, response):
        
        o = urlparse.urlparse(response.url)
        param_dict = urlparse.parse_qs(o.query)
        uk=int(param_dict['query_uk'][0])
        start=int(param_dict['start'][0])
        jp=json.loads(response.body)
        if jp['errno'] != 0 :
            self.log("GET baidu user sharelist error! errno:%d uk:%d url:%s"%(jp['errno'],uk,response.url),level=scrapy.log.WARNING)
            return

        if start ==0:
            self._setInvalid(uk,2,1)
        #print jp

        self.log("GET baidu user sharelist succ. uk:%s url:%s"%(uk,response.url),level=scrapy.log.INFO)
       
        #start=int(param_dict['start'][0])
        end=len(jp['records'])+start
        for record in jp['records']:
            if 'shorturl' not in record:
                record['shorturl']=''
            if record['feed_type']=='album':
                record['shareid']=""
                record['filelist']=[]
                for pp in record['operation']:
                    record['filelist'] += pp['filelist'] 
            else :
                record['album_id']=''
            yield BaiduShareItem(feed_type=record['feed_type'],
                                album_id=record['album_id'],
                                shareid=record['shareid'],
                                uk=record['uk'],
                                data_id=record['data_id'],
                                category=record['category'],
                                feed_time=record['feed_time'],
                                title=record['title'],
                                filecount=record['filecount'],
                                public=record['public'],
                                shorturl=record['shorturl'],
                                source_uid=record['source_uid'],
                                source_id=record['source_id'],
                                vCnt=record['vCnt'],
                                dCnt=record['dCnt'],
                                tCnt=record['tCnt'],
                                description=record['desc'],
                                is_valid=1,
                                last_crawl_time=str(datetime.datetime.now())
                        )
            for file in record['filelist']:
                yield BaiduFileItem(
                                        fs_id=file['fs_id'],
                                        uk=record['uk'],
                                        shareid=record['shareid'],
                                        album_id=record['album_id'],
                                        data_id=record['data_id'],
                                        server_filename=file['server_filename'],
                                        category=file['category'],
                                        isdir=file['isdir'],
                                        size=file['size'],
                                        path=file['path'],
                                        md5=file['md5'],
                                        sign=file['sign'],
                                        shorturl=record['shorturl'],
                                        is_valid=1,
                                        last_crawl_time=str(datetime.datetime.now())
                                        
                            )
                #if file['isdir']==1:
                 #   yield scrapy.Request('http://pan.baidu.com/share/list?uk=%s&shareid=%s&page=1&num=100&dir=%s&order=time&desc=1&_=%d&channel=chunlei&clienttype=0&web=1&app_id=250528'%(record['uk'],record['shareid'],file['path'],int(time.time())),
                  #                       callback=self.parseFile)
                
        #yield BaiduUserItem(uk=param_dict['query_uk'],table_action="update",)
        if end < jp['total_count']:
            yield self.reqeusetUserShareList(uk,end)
        else:
            self._setInvalid(uk,0,2)
            
    def parseFile(self,response):
        o = urlparse.urlparse(response.url)
        param_dict = urlparse.parse_qs(o.query)
        uk=int(param_dict['uk'][0])
        shareid=int(param_dict['shareid'][0])
        dir=param_dict['dir'][0]
        jp=json.loads(response.body)
        if jp['errno'] != 0 :
            self.log("GET baidu user sharelist error! errno:%d uk:%d url:%s"%(jp['errno'],uk,response.url),level=scrapy.log.WARNING)
            return

        for file in jp['list']:
                yield BaiduFileItem(
                                    fs_id=file['fs_id'],
                                    uk=uk,
                                    shareid=shareid,
                                    server_filename=file['server_filename'],
                                    category=file['category'],
                                    isdir=file['isdir'],
                                    size=file['size'],
                                    path=file['path'],
                                    md5=file['md5'],
                                    #sign=file['sign'],
                                    #time_stamp=file['time_stamp'],
                                    shorturl=record['shorturl']+'#path='+dir,
                                    last_crawl_time=str(datetime.datetime.now())
                                    
                        )
    
    def  parseUserInfo(self,response):
        jp=json.loads(response.body)
        if jp['errno'] != 0 :
            self.log("GET baidu user infor error! errno:%d url:%s"%(jp['errno'],response.url),level=scrapy.log.WARNING)
            return
        
        #print jp
        o = urlparse.urlparse(response.url)
        param_dict = urlparse.parse_qs(o.query)
        uk=int(param_dict['query_uk'][0])
        self.log("GET baidu user info succ. uk:%s url:%s"%(uk,response.url),level=scrapy.log.INFO)
        userinfo=jp['user_info']
        return BaiduUserItem(uk=uk,
                            username=userinfo["uname"],
                            pubshare_count=userinfo["pubshare_count"],
                            fans_count=userinfo["fans_count"],
                            follow_count=userinfo["follow_count"],
                            intro=userinfo["intro"],
                            album_count=userinfo["album_count"],
                            tui_user_count=userinfo["tui_user_count"],
                            c2c_user_sell_count=userinfo["c2c_user_sell_count"],
                            c2c_user_buy_count=userinfo["c2c_user_buy_count"],
                            c2c_user_product_count=userinfo["c2c_user_product_count"],
                            avatar_url=userinfo["avatar_url"],
                            last_insert_time=str(datetime.datetime.now())
                            )

    def  parseUserFanList(self,response):
        jp=json.loads(response.body)
        if jp['errno'] != 0 :
            self.log("GET baidu user fanlist error! errno:%d url:%s"%(jp['errno'],response.url),level=scrapy.log.WARNING)
            return
        
        #print jp
        o = urlparse.urlparse(response.url)
        param_dict = urlparse.parse_qs(o.query)
        uk=int(param_dict['query_uk'][0])
        start=int(param_dict['start'][0])
        fans_list=jp['fans_list']
        end=start+len(fans_list)
        
        self.log("GET baidu user fanlist succ. uk:%s url:%s"%(uk,response.url),level=scrapy.log.INFO)
        for userinfo in fans_list:
            
            yield BaiduUserItem(
                            uk=userinfo["fans_uk"],    
                            username=userinfo["fans_uname"],
                            pubshare_count=userinfo["pubshare_count"],
                            fans_count=userinfo["fans_count"],
                            follow_count=userinfo["follow_count"],
                            intro=userinfo["intro"],
                            album_count=userinfo["album_count"],
                            avatar_url=userinfo["avatar_url"],
                            last_insert_time=str(datetime.datetime.now())
                            )
            if "userFollowInfinite" in self.M_ACTIONS:
                yield self.requestUserFanList(userinfo["fans_uk"])
                yield self.requestUserFollowList(userinfo["fans_uk"])
            yield self.requestUserInfo(userinfo["fans_uk"])
            
        if end < jp['total_count']:
            yield self.requestUserFanList(uk,end)

    def  parseUserFollowList(self,response):
        jp=json.loads(response.body)
        if jp['errno'] != 0 :
            self.log("GET baidu user fanlist error! errno:%d url:%s"%(jp['errno'],response.url),level=scrapy.log.WARNING)
            return
        
        #print jp
        o = urlparse.urlparse(response.url)
        param_dict = urlparse.parse_qs(o.query)
        uk=int(param_dict['query_uk'][0])
        start=int(param_dict['start'][0])
        follow_list=jp['follow_list']
        end=start+len(follow_list)
        
        self.log("GET baidu user follow_list succ. uk:%s url:%s"%(uk,response.url),level=scrapy.log.INFO)
        for userinfo in follow_list:
            
            yield BaiduUserItem(
                            uk=userinfo["follow_uk"],    
                            username=userinfo["follow_uname"],
                            pubshare_count=userinfo["pubshare_count"],
                            fans_count=userinfo["fans_count"],
                            follow_count=userinfo["follow_count"],
                            intro=userinfo["intro"],
                            album_count=userinfo["album_count"],
                            avatar_url=userinfo["avatar_url"],
                            last_insert_time=str(datetime.datetime.now())
                            )
            if "userFollowInfinite" in self.M_ACTIONS:
                yield self.requestUserFanList(userinfo["follow_uk"])
                yield self.requestUserFollowList(userinfo["follow_uk"])         
            yield self.requestUserInfo(userinfo["follow_uk"])
        if end < jp['total_count']:
            yield self.requestUserFollowList(uk,end)
                        
    
class WangPanWuSpider(scrapy.Spider):
    name = "wangpanwu"
    allowed_domains = [ ]
    start_urls = []
    def start_requests(self):
        
        #print settings
      
        self.start_urls=self.settings.get('M_WANGPANWU_URLS')
            #pass
        self.rules=[
            (re.compile('^http://www.wangpanwu.com/p/list_\d\.html'),self._parse_user_list),
            (re.compile('^http://www.wangpanwu.com/p/fx/list_\d\.html'),self._parse_user_list),
            (re.compile('^http://www.wangpanwu.com/p/f\d+/'),self._parse_detail_page),
            (re.compile('^http://www.wangpanwu.com/zjgx/\w+/list_\d\.html'),self._parse_ziyuan_list),
            (re.compile('^http://www.wangpanwu.com/zjgx/list_\d\.html'),self._parse_ziyuan_list),
             
            ]
        return scrapy.Spider.start_requests(self)

    def parse(self,response):
        self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        for rule in self.rules:
            if rule[0].match(response.url):
                return rule[1](response)
                #print rule

        
            
    def _parse_user_list(self, response):
        ret_items=[]
        for sel in response.xpath('//span[@class="tou2"]'):
            
            link = sel.xpath('a/@href').extract()
            if link :
                uk=link[0].split("/")[2][1:]
               
                ret_items.append( BaiduUserItem(uk=uk,last_insert_time=str(datetime.datetime.now())))
                
        return ret_items
                
    def _parse_ziyuan_list(self,response):

        ret_items=[]
        for link in response.xpath('//span[@class="slink"]//a/@href').extract():
            yield scrapy.Request(link, callback=self._parse_detail_page)
 

    def _parse_detail_page(self,response):
        link=response.xpath('//div[@class="dr_box"]//a[1]/@href').extract()
        
        if link :
            uk=link[0].split("/")[2][1:]
            return BaiduUserItem(uk=uk,last_insert_time=str(datetime.datetime.now()))
                
       
