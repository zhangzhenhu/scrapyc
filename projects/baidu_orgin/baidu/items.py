# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import log
class DbItem(scrapy.Item):
    table_name=scrapy.Field()
    table_action=scrapy.Field()
    table_keys=scrapy.Field()
    table_primray_key=scrapy.Field()
    #_sql_str=None
    def __init__(self,*args,**kwargs):
        #print kwargs

        scrapy.Item.__init__(self,**kwargs)
        #self["table_action"]=""
        #self["table_name"]=""
    def _sql(self):
        if not self["table_name"] or not self["table_action"]:
            log.err("SQL: table_name or table_action is None")
            return None
        if self["table_action"] == "insert":
            n_str=""
            v_str=""
            for key_name in self["table_keys"]:
                if self.get(key_name):
                    n_str += key_name+","
                    v_str += "'%s'," %str(self.get(key_name)).replace("'","\\'")
                
            if v_str:
                _sql_str = "Insert into %s (%s) values (%s)  ON DUPLICATE KEY UPDATE " %(self["table_name"],n_str[:-1],v_str[:-1])
               # _sql_str = "REPLACE into %s (%s) values (%s)  where not exists(select * from %s where %s.%s = %s )" %(self["table_action"],self["table_name"],
                #    n_str[:-1],v_str[:-1],self["table_name"],self["table_name"],self["table_primray_key"],self.get(self["table_primray_key"]))
        elif self["table_action"] == "update" and self["table_primray_key"] and self.get(self["table_primray_key"]):
            
            v_str=""
            for key_name in self["table_keys"].keys():
                if key_name != self["table_primray_key"] and self.get(key_name):
            
                    v_str += key_name+"='"+str(self.get(key_name)).replace("'","\\'")+"'"
            if v_str:            
                _sql_str = "UPDATE %s SET %s WHERE %s=%s " %(self["table_name"],v_str,self["table_primray_key"],self.get(self["table_primray_key"]))
        
        return _sql_str

    def sql(self):
        if not self["table_name"] or not self["table_action"]:
            log.err("SQL: table_name or table_action is None")
            return None
        n_str=""
        v_str=""
        u_str=" "
        _sql_str=None
        for key_name in self["table_keys"]:

            if self.get(key_name) != None:
                n_str += key_name+","
                v_str += "'%s'," %unicode(self.get(key_name)).replace("'","\\'")
                if key_name != self["table_primray_key"]:            
                    u_str += " " + key_name+"='"+unicode(self.get(key_name)).replace("'","\\'")+"',"

        if v_str:
            _sql_str = "Insert into %s (%s) values (%s)  ON DUPLICATE KEY UPDATE %s" %(self["table_name"],n_str[:-1],v_str[:-1],u_str[:-1])
        return _sql_str

class SqlItem(DbItem):
    pass
class BaiduUserItem(DbItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uk = scrapy.Field()
    username = scrapy.Field()
    pubshare_count = scrapy.Field()
    secshare_cnt = scrapy.Field()
    fans_count = scrapy.Field()
    follow_count = scrapy.Field()
    intro = scrapy.Field()
    album_count = scrapy.Field()
    tui_user_count = scrapy.Field()
    c2c_user_sell_count = scrapy.Field()
    c2c_user_buy_count = scrapy.Field()
    c2c_user_product_count = scrapy.Field()
    avatar_url = scrapy.Field()
    last_insert_time = scrapy.Field()
    last_update_time= scrapy.Field()
    def __init__(self,*args,**kwargs):        
        DbItem.__init__(self,*args,**kwargs)
        
        self["table_primray_key"]="uk"
        self["table_name"] = "baidu_user"
        self["table_keys"]=["uk","username",
                            "pubshare_count",
                            "secshare_cnt",
                            "fans_count",
                            "follow_count",
                            "intro",
                            "album_count",
                            "tui_user_count",
                            "c2c_user_sell_count",
                            "c2c_user_buy_count",
                            "c2c_user_product_count",
                            "avatar_url",
                            "last_insert_time",
                            "last_update_time"]
        #datetime.datetime.now()
        
        
        
    

class BaiduShareItem(DbItem):
    # define the fields for your item here like:
    feed_type=scrapy.Field()
    album_id=scrapy.Field()
    shareid = scrapy.Field()
    uk = scrapy.Field()
    data_id = scrapy.Field()
    category = scrapy.Field()
    feed_time = scrapy.Field()
    title = scrapy.Field()
    filecount = scrapy.Field()
    public = scrapy.Field()
    shorturl = scrapy.Field()
    source_uid = scrapy.Field()
    source_id = scrapy.Field()
    vCnt = scrapy.Field()
    dCnt = scrapy.Field()
    tCnt = scrapy.Field()
    description = scrapy.Field()
    is_valid =  scrapy.Field()
    last_crawl_time= scrapy.Field()
    
    def __init__(self,*args,**kwargs):        
        DbItem.__init__(self,*args,**kwargs)
        
        self["table_primray_key"]="data_id"
        self["table_name"] = "baidu_share"
        self["table_keys"]=["shareid",'feed_type','album_id',
                            "uk",
                            "data_id",
                            "category",
                            "feed_time",
                            "title",
                            "filecount",
                            "public",
                            "shorturl",
                            "source_uid",
                            "source_id",
                            "vCnt",
                            "dCnt",
                            "tCnt",
                            "description",
                            'is_valid',
                            "last_crawl_time"]
        #datetime.datetime.now()

class BaiduFileItem(DbItem):
    # define the fields for your item here like:
    fs_id = scrapy.Field()
    uk = scrapy.Field()
    data_id = scrapy.Field()
    album_id = scrapy.Field()
    shareid = scrapy.Field()
    server_filename = scrapy.Field()
    category = scrapy.Field()
    isdir = scrapy.Field()
    size = scrapy.Field()
    path = scrapy.Field()
    md5 = scrapy.Field()
    sign = scrapy.Field()
    shorturl = scrapy.Field()
    is_valid=scrapy.Field()
    last_crawl_time= scrapy.Field()
    
    def __init__(self,*args,**kwargs):        
        DbItem.__init__(self,*args,**kwargs)
        
        self["table_primray_key"]="fs_id"
        self["table_name"] = "baidu_file"
        self["table_keys"]=["fs_id",'data_id','album_id',
                            "uk",
                            "shareid",
                            "server_filename",
                            "category",
                            "isdir",
                            "size",
                            "path",
                            "md5",
                            "sign",
                            "shorturl",
                            'is_valid',
                            "last_crawl_time"]
        #datetime.datetime.now()

