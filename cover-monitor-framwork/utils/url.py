



def get_url_site(url):
    if "://" in url:
        purl = url.split('://',1)[1]
    else:
        purl = url
    return purl.split("/",1)[0]

def replace_site(site):
    schema = ""
    if "://" in url[:10]:
        schema,url = url.split('://',1)
    url = url.split("/",1)[1]  

    if schema:
        return "%s://%s/%s"%(schema,site,url)
    else:
        return "%s/%s"%(site,url)