# -*- coding: utf-8 -*-

# Scrapy settings for shixin project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'shixin'

SPIDER_MODULES = ['shixin.spiders']
NEWSPIDER_MODULE = 'shixin.spiders'
LOG_FILE = "log.txt"
CONCURRENT_ITEMS = 100

CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 5
DOWNLOAD_DELAY = 0.5


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'


ITEM_PIPELINES = {
    'shixin.pipelines.ShixinPipeline': 30,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'shixin (+http://www.yourdomain.com)'
M_SQLDB_CONF={"host":"localhost","port":3306,"user":"wangpan","passwd":"wangpan","db":"shixin","charset":'utf8'}