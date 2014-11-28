# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from twisted.enterprise import adbapi
import datetime
import MySQLdb.cursors
from scrapy import log
from scrapy.exceptions import DropItem


class CsdnPipeline(object):
 
    def open_spider(self,spider):

        M_SQLDB_CONF = spider.settings.get("M_SQLDB_CONF")
        assert M_SQLDB_CONF, "Please set SQL DATABASE conf in baidu/settings.py ! eg:M_SQLDB_CONF={'host':'localhost','port':3306,'user':'wangpan','passwd':'wangpan','db':'wangpan'}"
         
        self.dbpool = adbapi.ConnectionPool('MySQLdb',cursorclass=MySQLdb.cursors.DictCursor,
                use_unicode=True,**M_SQLDB_CONF)
      
     
    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        
        return item
 
    def _conditional_insert(self, tx, item):
        # create record if doesn't exist. 
        # all this block run on it's own thread
        #tx.execute("select * from baidu_user where uk = %s", (item['uk'], ))
        #result = tx.fetchone()
        
        sql=item.sql()
        #log.msg("stored in db: table:%s action:%s sql:%s" % (item["table_name"],item["table_action"],sql), level=log.DEBUG)
        if not sql:
            return
        #print "[SQL]",sql
        tx.execute(sql)
        
        #log.msg("stored in db: table:%s action:%s sql:%s" % (item["table_name"],item["table_action"],sql), level=log.DEBUG)
 
    def handle_error(self, e):
        #print "-----------",e
        log.err(e)

