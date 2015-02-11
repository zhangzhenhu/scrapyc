# -*- coding: utf-8 -*-
from .strategy import Strategy
from utils.url import get_url_site,replace_site,remove_query,get_query
from utils.case import Case
import urllib

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
    

    def normaliz(self,url):
        if url.startswith("https://"):
            url = "http://" + url[8:]
        if "#" in url:
            url = url.split("#",1)[0]
        url = urllib.unquote(url).replace(" ","%20")
        return url


    def run(self,data):

        for case in data:

            origin = self.normaliz(case.target)
            site = get_url_site(origin)
            if site in ["m.facebook.com","id-id.facebook.com"]:
                if "profile.php?id=" in origin and "refsrc=" in origin:
                    refsrc = get_query(origin,"refsrc")
                    origin = urllib.unquote(refsrc.replace("%3A",":").replace("%2F","/")).replace(" ","%20")
                else:
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
                origin = remove_query(origin,"utm_term")
                origin = remove_query(origin,"utm_medium")
                origin = remove_query(origin,"hl")
                #case.add_common(origin)
                case.target = origin 
            elif site == "m.stafaband.info" :
                case.add_common(origin)
                case.target = replace_site(origin,"www.stafaband.info")             
            elif site == "m.olx.co.id":
                origin = remove_query(origin,"redirect")
                case.target = origin
            elif site == "anjingkita.com":
                case.add_common(origin)
                case.target = replace_site(origin,"www.anjingkita.com")

            REPLACE = self.settings["CONVERT_REPLACE"]
            if case.target in REPLACE:
                case.target = REPLACE[case.target]


            case.target = self.normaliz(case.target)


if __name__ == '__main__':
    data = [
    Case({},"https://id-id.facebook.com/notes/misteri-dunia/asteroid-aneh-buntuti-bumi-sejak-250-ribu-tahun-yang-lalu/10150099527477325"),
    ]
    Convert.run(data)
