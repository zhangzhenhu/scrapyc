# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import alibaba
import pymongo
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem
 
 
class MongoDBPipeline(object):
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB']
        #self.col = settings['MONGODB_COLLECTION']
        connection = pymongo.Connection(self.server, self.port)
        self.db = connection[self.db]
 
    def process_item(self, item, spider):
        err_msg = ''
        for field, data in item.items():
            if not data:
                err_msg += 'Missing %s of poem from %s\n' % (field, item['url'])
        if err_msg:
            raise DropItem(err_msg)
        print item.__class__.__name__  
        # collection = self.db[]
        # collection.insert(dict(item))
        # log.msg('Item written to MongoDB database %s/%s' % (self.db, self.col),
        #         level=log.DEBUG, spider=spider)
        return item
