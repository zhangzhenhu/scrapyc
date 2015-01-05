# -*- coding: utf-8 -*-

# Scrapy settings for alibaba project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
LOG_LEVEL = 'INFO'
BOT_NAME = 'alibaba'

SPIDER_MODULES = ['alibaba.spiders']
NEWSPIDER_MODULE = 'alibaba.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'


ITEM_PIPELINES = {
    #'scrapyc.server.utils.spider.sqlalchemypipelines.AlchemyPipeline':30,
    #'scrapyc.server.utils.spider.twistarpiplines.TwistarPipeline':30,
    'alibaba.pipelines.MongoDBPipeline': 30,
}
EXTENSIONS = {
'scrapyc.server.utils.spider.logstats.LogStats':200,
}
DOWNLOAD_DELAY = 5  
#LOG_FILE="log.txt"
CONCURRENT_REQUESTS=16
CONCURRENT_REQUESTS_PER_DOMAIN=4
CONCURRENT_REQUESTS_PER_IP=1




#M_SQLDB_CONF={"host":"localhost","port":3306,"user":"wangpan","passwd":"wangpan","db":"wangpan","charset":'utf8'}

#SQLALCHEMY_ENGINE_URL="mysql://wangpan:wangpan@localhost/wangpan?charset=utf8"
#SQLALCHEMY_CHARSET = "utf8"
#TWISTAR_DB_URL="MySQLdb://wangpan:wangpan@localhost/wangpan?charset=utf8"
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "alibaba"
