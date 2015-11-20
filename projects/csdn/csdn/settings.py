# -*- coding: utf-8 -*-

# Scrapy settings for csdn project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'csdn'

SPIDER_MODULES = ['csdn.spiders']
NEWSPIDER_MODULE = 'csdn.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'csdn (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'


ITEM_PIPELINES = {
    'csdn.pipelines.CsdnPipeline': 30,
}

DOWNLOAD_DELAY = 10  
#LOG_FILE="log.txt"
CONCURRENT_REQUESTS=16
CONCURRENT_REQUESTS_PER_DOMAIN=8
CONCURRENT_REQUESTS_PER_IP=1

M_SQLDB_CONF={"host":"localhost","port":3306,"user":"root","passwd":"root","db":"csdn","charset":'utf8'}