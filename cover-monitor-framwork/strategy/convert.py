# -*- coding: utf-8 -*-
from .strategy import Strategy
from utils.url import get_url_site,replace_site,remove_query
from utils.case import Case

def is_m1(url):
    up = url.split('?',1)
    if len(up) == 1:
        return False
    if 'm=1' in up[1]:
        return True
    return False

def remove_m1(url):
    url = url.replace("m=1","")
    if url[-1] == "?":
        url = url[:-1]
    return url

class Convert(Strategy):
    """docstring for Convert"""
    name = "convert"

    def run(self,data):

        for case in data:
            origin = case.target
            if origin.startswith("https://"):
                origin = "http://" + origin[8:]
            if "#" in origin:
                origin = origin.split("#",1)[0]
            case.target = origin

            site = get_url_site(origin)
            if site in ["m.facebook.com","id-id.facebook.com"]:
                origin = remove_query(origin,"refsrc")
                case.add_common(origin)
                case.target = replace_site(origin,"www.facebook.com")
                 

            elif site == "mobile.twitter.com":
                case.add_common(origin)
                case.target = replace_site(origin,"twitter.com")
            elif site == "m.youtube.com":
                case.add_common(origin)
                case.target = replace_site(origin,"www.youtube.com")
            elif site.endswith("blogspot.com")  and is_m1(origin):

                case.add_common(origin)
                case.target = remove_m1(origin) 
            elif site == "play.google.com":
                origin = remove_query(origin,"referrer")
                origin = remove_query(origin,"pcampaignid")
                #case.add_common(origin)
                case.target = origin            





if __name__ == '__main__':
    data = [
    Case({},"https://id-id.facebook.com/notes/misteri-dunia/asteroid-aneh-buntuti-bumi-sejak-250-ribu-tahun-yang-lalu/10150099527477325"),
    ]
    Convert.run(data)
