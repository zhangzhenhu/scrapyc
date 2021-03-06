import scrapy
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc, safe_url_string

from scrapy import signals
from robot.items import NimeiItem
from robot.spiders import base
from scrapy.utils.misc import load_object
from scrapyc.server.utils.url import get_url_site, get_url_scheme
import json
import urllib


class RpcSpider(base.RobotSpider):
    name = "rpc"
    allowed_domains = []
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(RpcSpider, self).__init__(*args, **kwargs)
        self._kwargs = kwargs

    def start_requests(self):

        fname = self.settings.get("INPUT_FILE", None)
        if fname:
            with open(fname) as fh:
                for line in fh.readlines():
                    url = line.strip().split()[0]
                    yield self.baidu_rpc_request({"url": url, "src_id": 22})
        url = self.settings.get("url", None)
        if url:
            yield self.baidu_rpc_request({"url": url, "src_id": 22})
