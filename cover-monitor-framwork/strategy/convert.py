# -*- coding: utf-8 -*-
from .strategy import Strategy
from utils.url import get_url_site,replace_site
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
            site = get_url_site(origin)
            if site == "m.facebook.com":
                case.add_common(replace_site(origin,"www.facebook.com"))
            elif site == "mobile.twitter.com":
                case.add_common(replace_site(origin,"twitter.com"))
            elif site == "m.youtube.com":
                case.add_common(replace_site(origin,"www.youtube.com"))
            elif site.endswith("blogspot.com")  and is_m1(origin):
                case.add_common(remove_m1(origin) )    





        pass