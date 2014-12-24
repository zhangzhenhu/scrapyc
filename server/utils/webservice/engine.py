from scrapy.webservice import JsonRpcResource
from scrapy.http import Request
class EngineResource(JsonRpcResource):

    ws_name = 'engine'

    def __init__(self, crawler):
        JsonRpcResource.__init__(self, crawler, self)


    def crawl(self,req,spider=None):
        """ req is a  dict that pass to scrapy Request:
            http://scrapy-chs.readthedocs.org/zh_CN/0.24/topics/request-response.html#scrapy.http.Request
            but the callback param is invalid.
        """
        open_spiders = self.crawler.engine.open_spiders
        if not open_spiders:
            return False,"no open spiders"
        if spider == None:
            spider = open_spiders[0]
        else:
            for o_spider  in open_spiders:
                if o_spider.name == spider:
                    spider = o_spider
        if not spider:
            return False,"wrong spider"
            
        self.crawler.engine.crawl(Request(**req),spider)
        return True,"succeess"
        
