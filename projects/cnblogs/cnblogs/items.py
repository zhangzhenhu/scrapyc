# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CnblogsItem(scrapy.Item):
    table_name=scrapy.Field()
    table_action=scrapy.Field()
    table_keys=scrapy.Field()
    table_primray_key=scrapy.Field()
    #_sql_str=None
    def __init__(self,*args,**kwargs):
        scrapy.Item.__init__(self,**kwargs)

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


class CnblogsUserItem(CnblogsItem):
    username=scrapy.Field()
    avatar_url=scrapy.Field()
    last_insert_time = scrapy.Field()
    last_update_time= scrapy.Field()
    def __init__(self,*args,**kwargs):
        CnblogsItem.__init__(self,*args,**kwargs)
        
        self["table_primray_key"] = "username"
        self["table_name"] = "user"
        self["table_keys"] = ["username","avatar_url","last_insert_time","last_update_time"]

class CnblogsArticleItem(CnblogsItem):
    username=scrapy.Field()
    article_id = scrapy.Field()
    article_url=scrapy.Field()
    article_title = scrapy.Field()
    article_description = scrapy.Field()
    postdate = scrapy.Field()
    view = scrapy.Field()
    comments = scrapy.Field()
    last_insert_time = scrapy.Field()
    last_update_time= scrapy.Field()
    def __init__(self,*args,**kwargs):
        CnblogsItem.__init__(self,*args,**kwargs)
        
        self["table_primray_key"] = "article_id"
        self["table_name"] = "article_list"
        self["table_keys"] = ["username","article_url","article_id",
        "article_title",
        'article_description',
        'postdate',
        'view',
        'comments',
        "last_insert_time","last_update_time"]