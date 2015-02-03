# -*- coding: utf-8 -*-
from .strategy import Strategy


class Linkbase(Strategy):
    """docstring for Linkbase"""
    name = "linkbase"

    def run(self,data):

        for case in data:
            if case.close:
                continue
            ld = case.get_data("linkbase")
            l2patch = case.get_data("l2patch")
            l2base = case.get_data("l2base")
            if ld and l2patch and l2base and ld.get("urlnew") == "-" and  l2patch.get("urlnew") == "-" and  l2base.get("urlnew") == "-":
                    case.set_result("conclusion","notFound")
                    case.close = True
                    continue
            if ld:
                urlnew = ld.get("urlnew")
                if urlnew == "CHK" :
                    case.set_result("conclusion","lcDiff")
                    case.close = True
                    continue
                elif urlnew == "GET":
                    url_level  = ld.get("url_level")
                    forceGET  = ld.get("forceGET")
                    crawl_fail = ld.get("crawl_fail")
                    if crawl_fail == True:
                        case.set_result("conclusion","crawlFail")
                        case.set_result("reason","crawl_total:%d&&crawl_fail:%d"%(ld.get("craw_count"),ld.get("fail_count")))                       
                    elif url_level in ["1","0"]:
                        case.set_result("conclusion","lowLevel")
                        case.set_result("reason","url_level=%s"%url_level)
                    else:
                        case.set_result("reason","urlnew=GET&&url_level=%s&&forceGET=%s"%(url_level,forceGET))
                        case.set_result("conclusion","unCrawl")
                    case.close = True
                    continue

            if l2patch and "del_reason" in l2patch and l2patch["del_reason"] != "-" :
                case.set_result("conclusion","linkbaseDel")
                case.set_result("reason","del_reason="+l2patch["del_reason"])
                case.close = True
                continue
            
            if l2base and "del_reason" in l2base and l2base["del_reason"] != "-" :
                case.set_result("conclusion","linkbaseDel")
                case.set_result("reason",l2base["del_reason"])
                case.close = True
                continue



        pass