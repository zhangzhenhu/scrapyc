# -*- coding: utf-8 -*-

# Scrapy settings for nimei project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'mtime'
LOG_LEVEL = 'INFO'
SPIDER_MODULES = ['mtime.spiders']
NEWSPIDER_MODULE = 'mtime.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nimei (+http://www.yourdomain.com)'

EXTENSIONS = {
    # 把爬虫的统计信息dump到一个指定的文件中，方便srapyc平台进行读取
    # 文件的路径由scrapyc自动通过命令行参数传入
    'scrapyc_contrib.spider.logstats.LogStats' : 200,
}

DATA_ENCODING="utf8"
#DOWNLOAD_HANDLERS={'http':'scrapyc.server.utils.PhantomJSDownloadHandler.PhantomJSDownloadHandler',}

FEED_EXPORTERS = {
    "mtime":'mtime.pipelines.FileItemExporter'
}
LOGSTATS_DUMP_FILE = "/home/zhangzhenhu/mtime/stats.log"
FEED_URI = "file:///home/zhangzhenhu/mtime/url-people.txt"
FEED_FORMAT = "mtime"

HBASE_SERVER = "localhost"
import socket
if "baidu.com " in socket.gethostname():
    HBASE_SERVER = 'st01-ps-ssd2145.st01.baidu.com'
    LOGSTATS_DUMP_FILE = "/home/spider/zhangzhenhu/mtime/stats.log"
    FEED_URI = "file:///home/spider/zhangzhenhu/mtime/url-people.txt"
    import sys
    sys.path.append('/home/spider/zhangzhenhu/github/scrapyc')
