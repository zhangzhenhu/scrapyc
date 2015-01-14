



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

if __name__ == '__main__':
    print remove_query("http://m.facebook.com/jituharian?refsrc=id-id.facebook.com/jituharian","refsrc")