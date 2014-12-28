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
    charset="utf-8"
    def __init__(self, *args, **kwargs):
        super(TwistarItem, self).__init__(*args, **kwargs)
        self._instance = None
        self._errors = None


    @property
    def dbobject(self):
        if self._instance is None:
            # modelargs = dict((k, self.get(k)) for k in self._values
            #                  if k in self._model_fields)
            args={}
            for key,value in self.items():
                if isinstance(value,unicode):
                    value=value.encode(self.charset)
                args[key] = value
            self._instance = self.sql_model(**args)
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
        self.log("[process item] %s"%item,level=log.DEBUG )
        #if isinstance(item,TwistarItem):
        def _save_ok(obj):
            self.log("[save item succeed] %s"%obj,level=log.DEBUG )
        
        def _save_err(obj):
            self.log("[save item failed] %s"%obj,level=log.ERROR )

        def _update(sobj,tobj):
            if sobj:
                tobj.id=sobj[0].id
            self.log("[update item] %s"%tobj,level=log.DEBUG )
            defer = tobj.save()
            defer.addCallback(_save_ok)
            defer.addErrback(_save_err)

        if item.uniq_filter:
            item.dbcls.findBy(**item.uniq_filter).addCallback(_update,item.dbobject)
        else:
            defer=item.dbobject.save()
            defer.addCallback(_save_ok)
            defer.addErrback(_save_err)

        return item