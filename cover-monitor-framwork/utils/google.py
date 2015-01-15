import time
import datetime
import os
import urllib2
import re
import cookielib
import StringIO
import gzip    
import urlparse
import sys
import urllib
import lxml.html
import lxml.etree
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
urllib2.install_opener(opener)
#httpHandler = urllib2.HTTPHandler(debuglevel=1)
#opener = urllib2.build_opener(httpHandler)
#urllib2.install_opener(opener) 
def pget(url):
    req=urllib2.Request(url)
    #scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
    #req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36")
    req.add_header("User-Agent","Mozilla/5.0 (Linux;u;Android 2.3.7;zh-cn;) AppleWebKit/533.1 (KHTML,like Gecko) Version/4.0 Mobile Safari/533.1 (compatible; +http://www.baidu.com/search/spi_der.html)")
    #re.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    req.add_header("Accept-Encoding","gzip,deflate,sdch")
    #re.add_header("Accept-Language","zh-CN,zh;q=0.8,en;q=0.6")
    #req.add_header("Host")
    req.add_header("Cache-Control","no-cache")
    req.add_header("Pragma","no-cache")
    req.add_header("Connection","keep-alive")
    #pdb.set_trace()
    Sleep_Time = 1
    retry=1
    while retry < 10:
        time.sleep(Sleep_Time)
        try:
            ret=urllib2.urlopen(req,timeout=10)
            if ret.getcode() /100 !=2 :
                print "[wget] failed url:%s retcode:%d" % (url,ret.getcode())
                retry += 1
                time.sleep(Sleep_Time*5)
                continue
            print "[wget] succed url:%s retcode:%d" % (url,ret.getcode())
            reply=ret.info()
            if reply.getheader("Content-Encoding")=="gzip":
                compresseddata = ret.read()
                compressedstream = StringIO.StringIO(compresseddata)
                gzipper = gzip.GzipFile(fileobj=compressedstream)
                
                data=gzipper.read()
                ret.close()
                return  data
            
            data=ret.read()
            ret.close()
            return data
        except  Exception,e:
            print "[wget] error url:%s errcode:%s" % (url,e)
        time.sleep(2)
        retry += 1
    return None

def get_url_query(url):
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
    if not query:
        return {}
    ret = {}
    for item in query.split("&"):
        item = item.strip()
        if not item:
            continue
        item = item.split('=',1)
        if len(item) == 2:
            ret[item[0]] =item[1]
        else:
            ret[item[0]] = None
    return ret

def parse(html):
    tree=lxml.html.fromstring(html.decode("utf8"))

    for href in tree.xpath('//li[@class="g card-section"]//h3/a/@href'):
        yield href
        # continue
        # qs = get_url_query(href)
        # if 'url' not in qs:
        #     continue
        # yield urllib.unquote(qs['url'])


def main():
    for query in sys.stdin:
        query = query.strip()
        en_query = urllib.quote(query)
        print en_query
        furl = URL_TEMPLATE%{"query":en_query}
        html = pget(furl)
        if  not html:
            continue
        index = 0
        for url in parse(html):
            print "%s\t%s\t%d\t%s"%(furl,url,index,query)
            index += 1


if __name__ == '__main__':
    URL_TEMPLATE = 'http://www.google.co.id/search?hl=ar-eg&start=0&q=%(query)s&num=100&nord=1'

    main()