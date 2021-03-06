# -*- coding: utf-8 -*-

# Scrapy settings for robot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'robot'
LOG_LEVEL = 'DEBUG'
SPIDER_MODULES = ['robot.spiders']
NEWSPIDER_MODULE = 'robot.spiders'


import os
import sys
from importlib import import_module
from os.path import join, abspath, dirname
import logging

WORK_PATH=os.getcwd()
LOG_PATH = os.path.join(WORK_PATH,"log")
DATA_PATH = os.path.join(WORK_PATH,"data")
PROJECT_PATH = os.path.join(WORK_PATH,"projects")
HISTORY_PATH = os.path.join(WORK_PATH,"history")
LOG_LEVEL = logging.INFO
LOG_FORMATER = "%(asctime)s [%(filename)s::%(funcName)s:%(lineno)d] %(levelname)s %(message)s"
MAX_RUN_TASK = 10

#需要配置JOBDIR才会使用磁盘队列
#JOBDIR = os.path.join(HISTORY_PATH,str(os.getpid()))
# if not os.path.exists(JOBDIR):
#     os.makedirs(JOBDIR)
CONCURRENT_REQUESTS=100
CONCURRENT_REQUESTS_PER_DOMAIN=100
CONCURRENT_REQUESTS_PER_IP=0
DOWNLOAD_DELAY=0
RANDOMIZE_DOWNLOAD_DELAY=True
DNSCACHE_ENABLED=True
LOG_ENCODING="gbk"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'
EXTENSIONS = {
#'scrapyc.server.utils.logstats.LogStats':200,
}
ALLOW_SITES=[]
FEED_URI="file:///home/spider/zhangzhenhu/robot/%(name)s/%(time)s.json"
#FEED_FORMAT="jsonlines"
#MAX_DEPTH = 2
#DEPTH_LIMIT = 10
DEPTH_PRIORITY = 0
#DOWNLOAD_HANDLERS={'http':'scrapyc.server.utils.PhantomJSDownloadHandler.PhantomJSDownloadHandler',}
DOWNLOAD_TIMEOUT = 360
WEBSERVICE_PORT=9885
WEBSERVICE_ENABLED=0
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.chunked.ChunkedTransferMiddleware': 53,
    'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware':54
}
INPUT_FILE=None
BAIDU_RPC_SERVER_URL=[
"http://yq01-ps-exdata-svr00.yq01.baidu.com:8004/ExdataService/Exdata",
"http://yq01-ps-exdata-svr01.yq01.baidu.com:8004/ExdataService/Exdata",
"http://yq01-ps-exdata-svr02.yq01.baidu.com:8004/ExdataService/Exdata",
"http://yq01-ps-exdata-svr03.yq01.baidu.com:8004/ExdataService/Exdata",
"http://yq01-ps-exdata-svr04.yq01.baidu.com:8004/ExdataService/Exdata",
"http://yq01-ps-exdata-svr05.yq01.baidu.com:8004/ExdataService/Exdata",
"http://yq01-ps-exdata-svr06.yq01.baidu.com:8004/ExdataService/Exdata",
"http://yq01-ps-exdata-svr07.yq01.baidu.com:8004/ExdataService/Exdata",
"http://yq01-ps-exdata-svr08.yq01.baidu.com:8004/ExdataService/Exdata",
"http://yq01-ps-exdata-svr09.yq01.baidu.com:8004/ExdataService/Exdata",
]
SITE_SPIDERS = {
    #"211.103.242.133:8080":"robot.spiders.211-103-242-133.Parser",
    #"www.weihai.gov.cn":"robot.spiders.weihai.Parser"
    "www.im286.com":"robot.spiders.bbs.Parser"

}