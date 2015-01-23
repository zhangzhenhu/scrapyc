import json
import sys


def get_url_schema(url):
    if "://" in url[:10]:
        return url[:10].split("://")[0]
    return ""

for line in sys.stdin:
    try:
        item = json.loads(line.strip())
        url = item["url"].encode("utf8")
        if get_url_schema(url) not in ["http","https"]:
            continue
        print url
    #print item["fromurl"]
    except:
        pass
