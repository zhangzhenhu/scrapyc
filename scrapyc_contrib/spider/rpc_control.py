"""
Example script to control a Scrapy server using its JSON-RPC web service.

It only provides a reduced functionality as its main purpose is to illustrate
how to write a web service client. Feel free to improve or write you own.

Also, keep in mind that the JSON-RPC API is not stable. The recommended way for
controlling a Scrapy server is through the execution queue (see the "queue"
command).

"""

from __future__ import print_function
import sys, optparse, urllib, json
from urlparse import urljoin
try:
    from scrapy.utils.jsonrpc import jsonrpc_client_call, JsonRpcError
except:
    from scrapy_jsonrpc.jsonrpc import jsonrpc_client_call, JsonRpcError


def cmd_stop(host="127.0.0.1",port=0,spider=None):
    """stop <spider> - stop a running spider"""
    return jsonrpc_call(host,port, 'crawler/engine', 'close_spider',spider)

def cmd_list_running(args, opts):
    """list-running - list running spiders"""
    for x in json_get(host,port, 'crawler/engine/open_spiders'):
        print(x)

def cmd_list_available(args, opts):
    """list-available - list name of available spiders"""
    for x in jsonrpc_call(host,port, 'crawler/spiders', 'list'):
        print(x)

def cmd_list_resources(args, opts):
    """list-resources - list available web service resources"""
    for x in json_get(host,port, '')['resources']:
        print(x)

def cmd_get_spider_stats( spider,host="127.0.0.1",port=0):
    """get-spider-stats <spider> - get stats of a running spider"""
    stats = jsonrpc_call(host,port, 'stats', 'get_stats', spider)
    return stats
    for name, value in stats.items():
        print("%-40s %s" % (name, value))

def cmd_get_global_stats(host="127.0.0.1",port=0):
    """get-global-stats - get global stats"""
    stats = jsonrpc_call(host,port, 'stats', 'get_stats')
    return stats
    for name, value in stats.items():
        print("%-40s %s" % (name, value))

def get_wsurl(host,port, path):
    return urljoin("http://%s:%s/"% (host, port), path)

def jsonrpc_call(host,port, path, method, *args, **kwargs):
    url = get_wsurl(host,port, path)
    return jsonrpc_client_call(url, method, *args, **kwargs)

def json_get(opts, path):
    url = get_wsurl(opts, path)
    return json.loads(urllib.urlopen(url).read())


