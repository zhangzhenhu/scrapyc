# -*- coding: utf-8 -*-
from .strategy import Strategy
from utils.url import get_url_site

class Forbid(Strategy):
    """docstring for Forbid"""
    def run(self,data):
        for case in data:
            if case.close and case.result.get("conclusion") in ["noProblem"]:
                continue
            # robots = case.get_data("robots")
            # if  not robots or robots.get('robots') != "DISALLOW":
            #     return
            site = get_url_site(case.target)
            if ".wapka.me" in site  or ".wapka.mobi" in site:
                case.set_result("conclusion","Forbidden")
                case.set_result("reason","ip")
                case.close = True
                continue
            forbid = case.get_data("forbid")
            if not forbid:
                continue
            if "forbidden" in forbid and forbid["forbidden"]:
                case.set_result("conclusion","Forbidden")
                case.set_result("reason",forbid["forbidden"])
                if "out" in forbid and forbid["out"]:
                    case.set_result("conclusion","Forbidden_nm")
                    case.set_result("additional","out:%s"%(forbid["out"]))
                case.close = True
        return                