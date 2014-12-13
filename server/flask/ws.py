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

from scrapy.utils.jsonrpc import jsonrpc_client_call, JsonRpcError




def cmd_stop(args, opts):
    """stop <spider> - stop a running spider"""
    jsonrpc_call(opts, 'crawler/engine', 'close_spider', args[0])

def cmd_list_running(args, opts):
    """list-running - list running spiders"""
    for x in json_get(opts, 'crawler/engine/open_spiders'):
        print(x)

def cmd_list_available(args, opts):
    """list-available - list name of available spiders"""
    for x in jsonrpc_call(opts, 'crawler/spiders', 'list'):
        print(x)

def cmd_list_resources(args, opts):
    """list-resources - list available web service resources"""
    for x in json_get(opts, '')['resources']:
        print(x)

def cmd_get_spider_stats( host="127.0.0.1",port,args):
    """get-spider-stats <spider> - get stats of a running spider"""
    stats = jsonrpc_call(opts, 'stats', 'get_stats', args[0])
    return stats
    for name, value in stats.items():
        print("%-40s %s" % (name, value))

def cmd_get_global_stats(host="127.0.0.1",port,args=[])
    """get-global-stats - get global stats"""
    stats = jsonrpc_call(host="127.0.0.1",port, 'stats', 'get_stats',*args)
    return stats
    for name, value in stats.items():
        print("%-40s %s" % (name, value))

def get_wsurl(host="127.0.0.1",port, path):
    return urljoin("http://%s:%s/"% (host, port), path)

def jsonrpc_call(host="127.0.0.1",port, path, method, *args, **kwargs):
    url = get_wsurl(host="127.0.0.1",port, path)
    return jsonrpc_client_call(url, method, *args, **kwargs)

def json_get(opts, path):
    url = get_wsurl(opts, path)
    return json.loads(urllib.urlopen(url).read())


