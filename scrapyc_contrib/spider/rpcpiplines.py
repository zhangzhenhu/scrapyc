#encoding=utf8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.utils.jsonrpc import jsonrpc_client_call, JsonRpcError


class RpcPipeline(object):

    def open_spider(self,spider):
        self.settings =  spider.settings
        self.rpc_url = self.settings["RPCPIPLINE_URL"]
        self.rpc_method = self.settings["RPCPIPLINE_METHOD"]

        

    def process_item(self, item, spider):
        jsonrpc_client_call(self.rpc_url, self.rpc_method, *args, **kwargs)

        return item