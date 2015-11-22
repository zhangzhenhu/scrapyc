# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import BaseItemExporter

class NimeiPipeline(object):
    def process_item(self, item, spider):
        return item


class FileItemExporter(BaseItemExporter):

    def __init__(self, file, **kwargs):
        self._configure(kwargs)
        self.file = file

    def export_item(self, item):
        itemdict = dict(self._get_serialized_fields(item))
        msg = []
        if 'key' in itemdict:
            msg.append(itemdict['key'])
        for key, value in itemdict.iteritems():
            if key == "key":
                continue
            msg.append("%s:%s" %(key, value))

        msg.append('\n')
        self.file.write("\t".join(msg))