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


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'robot (+http://www.yourdomain.com)'
EXTENSIONS = {
#'scrapyc.server.utils.logstats.LogStats':200,
}
FEED_URI="file:///home/spider/zhangzhenhu/robot/%(name)s/%(time)s.json"
FEED_FORMAT="jsonlines"
MAX_DEPTH = 2
DEPTH_LIMIT=2
DEPTH_PRIORITY = 1
#DOWNLOAD_HANDLERS={'http':'scrapyc.server.utils.PhantomJSDownloadHandler.PhantomJSDownloadHandler',}
WEBSERVICE_PORT=9805
WEBSERVICE_ENABLED=1