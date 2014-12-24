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

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'robot (+http://www.yourdomain.com)'
EXTENSIONS = {
'scrapyc.server.utils.logstats.LogStats':200,
}
#DOWNLOAD_HANDLERS={'http':'scrapyc.server.utils.PhantomJSDownloadHandler.PhantomJSDownloadHandler',}