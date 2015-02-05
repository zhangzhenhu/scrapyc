# -*- coding: utf-8 -*-
from .strategy import Strategy
from utils.url import get_url_site

class Forbid(Strategy):
    """docstring for Forbid"""
    def run(self,data):
        for case in data:
            if case.close:
                continue
            # robots = case.get_data("robots")
            # if  not robots or robots.get('robots') != "DISALLOW":
            #     return
            site = get_url_site(case.target)
            if ".wapka.me" in site  or ".wapka.mobi" in site:
                case.set_result("conclusion","ipForbidden")
                case.set_result("reason","ip")
                case.close = True
        return                