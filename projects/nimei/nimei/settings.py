# -*- coding: utf-8 -*-

# Scrapy settings for nimei project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'nimei'
LOG_LEVEL = 'DEBUG'
SPIDER_MODULES = ['nimei.spiders']
NEWSPIDER_MODULE = 'nimei.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nimei (+http://www.yourdomain.com)'
EXTENSIONS = {
'scrapyc_contrib.spider.logstats.LogStats':200,
}
#DOWNLOAD_HANDLERS={'http':'scrapyc.server.utils.PhantomJSDownloadHandler.PhantomJSDownloadHandler',}