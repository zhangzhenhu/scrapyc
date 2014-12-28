# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

#encoding=utf8
from twisted.enterprise import adbapi
from twistar.registry import Registry
from twistar.dbobject import DBObject
from scrapy.conf import settings
from ..url import parse_sql_url,translate_connect_args
from scrapy.item import Field, Item, ItemMeta
from scrapy import log
class TwistarItemMeta(ItemMeta):

    def  __new__(mcs, class_name, bases, attrs):
        cls = super(TwistarItemMeta, mcs).__new__(mcs, class_name, bases, attrs)
        #cls.fields = cls.fields.copy()
        if cls.sql_model:
            cls._model_fields = []
            #cls._model_meta = cls.sqlalchemy_model._meta
            tablename = cls.sql_model.tablename
            #attrs = {}
            if Registry.SCHEMAS.has_key(tablename):
                for name in Registry.SCHEMAS[tablename]:
                    if name not in cls.fields:
                        cls.fields[name] = Field()
                    cls._model_fields.append(name)
        return cls


class TwistarItem(Item):

    #__metaclass__ = TwistarItemMeta

    #a DBObject class
    sql_model = None

    def __init__(self, *args, **kwargs):
        super(TwistarItem, self).__init__(*args, **kwargs)
        self._instance = None
        self._errors = None


    @property
    def dbobject(self):
        if self._instance is None:
            # modelargs = dict((k, self.get(k)) for k in self._values
            #                  if k in self._model_fields)

            self._instance = self.sql_model(**self)
        return self._instance

    @property
    def dbcls(self):
        return self.sql_model
    @property
    def uniq_filter(self):
        pass


#TWISTAR_DB_URL="MySQLdb://wangpan:wangpan@localhost/wangpan?charset=utf8"
class TwistarPipeline(object):

    def open_spider(self,spider):
        self.settings =  spider.settings
        self.log=spider.log
        sql_url = settings['TWISTAR_DB_URL']
        conn_arg = parse_sql_url(sql_url)
        drivername = conn_arg.pop("drivername")
        conn_arg = translate_connect_args(drivername,**conn_arg)
        try:
            conn_arg["port"] = int(conn_arg["port"])
        except:
            conn_arg["port"] = 3306

        Registry.DBPOOL = adbapi.ConnectionPool(drivername, **conn_arg)


        

    def process_item(self, item, spider):
        self.log("[process item] %s"%item,level=log.INFO )
        if isinstance(item,TwistarItem):
            def _save_done(obj):
                self.log("[save item] %s"%obj,level=log.INFO )

            def _pre_save(sobj,tobj):
                if sobj:
                    tobj.id=sobj[0].id
                tobj.save().addCallback(_save_done)
            if item.uniq_filter:
                item.dbcls.findBy(**item.uniq_filter).addCallback(_pre_save,item.dbobject)
            else:
                item.dbobject.save().addCallback(_save_done)

        return item