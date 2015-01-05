



def get_url_site(url):
    if "://" in url:
        purl = url.split('://')[1]
    else:
        purl = url
    return purl.split("/")[0]
    