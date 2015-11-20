# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json

class BaseItem(scrapy.Item):
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

class ShixinItem(BaseItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    iname = scrapy.Field()
    caseCode = scrapy.Field()
    age = scrapy.Field()
    sexy = scrapy.Field()
    focusNumber = scrapy.Field()
    cardNum = scrapy.Field()
    courtName = scrapy.Field()
    areaName = scrapy.Field()
    businessEntity = scrapy.Field()
    partyTypeName = scrapy.Field()
    regDate = scrapy.Field()
    gistId = scrapy.Field()
    gistUnit = scrapy.Field()
    duty=scrapy.Field()
    performance = scrapy.Field()
    disruptTypeName = scrapy.Field()
    publishDate = scrapy.Field()
    performedPart = scrapy.Field()
    unperformPart = scrapy.Field()
    person_or_unit = scrapy.Field()
    last_crawl_time= scrapy.Field()
    
    def __init__(self,*args,**kwargs):        
        BaseItem.__init__(self,*args,**kwargs)
        self["table_action"] = "insert"
        self["table_primray_key"]="id"
        self["table_name"] = "shixin"
        self["table_keys"]=["id","iname","cardNum","caseCode","age","sexy","focusNumber","areaName","businessEntity","courtName","duty","performance","disruptTypeName","publishDate","partyTypeName","gistId","regDate","gistUnit","performedPart","unperformPart","person_or_unit","last_crawl_time"]
        #datetime.datetime.now()
    @classmethod
    def from_json(cls,jp):
        item = cls()
        for key,value in json.loads(jp).items():
            item[key]=value
        return item



"""
create table shixin (
    id BIGINT UNSIGNED NOT NULL unique PRIMARY KEY, 
    iname VARCHAR(254),
    caseCode  VARCHAR(1024),
    age INT UNSIGNED,
    sexy VARCHAR(10),
    focusNumber INT UNSIGNED,
    cardNum VARCHAR(255),
    courtName VARCHAR(2048),
    areaName VARCHAR(2048),
    businessEntity VARCHAR(2048),
    partyTypeName VARCHAR(255),
    regDate VARCHAR(255),
    gistId VARCHAR(2048),
    gistUnit VARCHAR(2048),
    duty Text,
    performance VARCHAR(2048),
    disruptTypeName VARCHAR(2048),
    publishDate VARCHAR(255),
    performedPart VARCHAR(255),
    unperformPart VARCHAR(255),
    person_or_unit VARCHAR(10),
    last_crawl_time DATETIME
    )
"""