



def get_url_site(url):
    if "://" in url:
        purl = url.split('://',1)[1]
    else:
        purl = url
    return purl.split("/",1)[0]

def replace_site(url,site):
    schema = ""
    if "://" in url[:10]:
        schema,url = url.split('://',1)
    url = url.split("/",1)[1]  

    if schema:
        return "%s://%s/%s"%(schema,site,url)
    else:
        return "%s/%s"%(site,url)
def remove_query(url,qname):
    nurl = url.split("?",1)
    if len(nurl) == 1 or not nurl[1]:
        return url
    nq = ""
    qname = qname + "="
    for item in nurl[1].split('&'):
        if item.startswith(qname):
            continue
        nq += item + "&"
    if nq:
        return nurl[0] + "?" + nq[:-1]
    return nurl[0]
def get_query(url,qname):
    nurl = url.split("?",1)
    if len(nurl) == 1 or not nurl[1]:
        return None
    nq = ""
    qname = qname + "="
    for item in nurl[1].split('&'):
        if item.startswith(qname):
            item = item.split("=")
            if len(item) > 1: return item[1]
            return None
    return None


import time
import datetime
import os
import urllib2
import re
import cookielib
import StringIO
import gzip    
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
urllib2.install_opener(opener)
#httpHandler = urllib2.HTTPHandler(debuglevel=1)
#opener = urllib2.build_opener(httpHandler)
#urllib2.install_opener(opener) 
def pget(url):
    req=urllib2.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36")
    #re.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    req.add_header("Accept-Encoding","gzip,deflate,sdch")
    #re.add_header("Accept-Language","zh-CN,zh;q=0.8,en;q=0.6")
    req.add_header("Host","www.okooo.com")
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

if __name__ == '__main__':
    print remove_query("http://m.facebook.com/jituharian?refsrc=id-id.facebook.com/jituharian","refsrc")