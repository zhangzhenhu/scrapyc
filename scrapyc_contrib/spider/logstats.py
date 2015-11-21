# -*- coding: utf-8 -*-
"""
把爬虫的统计信息dump到一个指定的文件中，方便srapyc平台进行读取
文件的路径有scrapyc自动通过命令行参数传入

发布到scrapyc的爬虫需要在爬虫的setting文件中加入本扩展
EXTENSIONS = {
'scrapyc_contrib.spider.logstats.LogStats':200,
}

Authors: acmtiger@gmail.com
Date:    2015/11/16 9:42
"""
from twisted.internet import task

from scrapy.exceptions import NotConfigured
from scrapy import log, signals
import os, cPickle as pickle


class LogStats(object):
    """Log basic scraping stats periodically"""

    def __init__(self, stats, dump_file=None):
        self.stats = stats
        self.dump_file = dump_file
        #self.multiplier = 60.0 / self.interval

    @classmethod
    def from_crawler(cls, crawler):
        dump_file = crawler.settings.get('LOGSTATS_DUMP_FILE')
        if not dump_file:
           raise NotConfigured
        o = cls(crawler.stats, dump_file)
        #crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        return


    def log(self, spider):
        if self.dump_file:
            with open(self.dump_file, 'wb') as f:
                pickle.dump(self.stats.get_stats(), f, protocol=2)

    def spider_closed(self, spider, reason):
        self.log(spider)
        #if self.task.running:
         #   self.task.stop()
