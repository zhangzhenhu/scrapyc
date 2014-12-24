# -*- coding: utf-8 -*-

# Scrapy settings for nimei project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#



EXTENSIONS = {
'scrapyc.server.utils.logstats.LogStats':200,
}

#PhantomJS
DOWNLOAD_HANDLERS={'http':'scrapyc.server.utils.spider.phantomjsdownloadhandler.PhantomJSDownloadHandler',}

#RpcPipeline
RPCPIPLINE_URL=http://${HOST}:${PORT}/
RPCPIPLINE_METHOD="add_url"