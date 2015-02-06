# -*- coding: utf-8 -*-
from .strategy import Strategy
from utils.url import get_url_site


class IP(Strategy):
    """docstring for IP"""
    def run(self,data):
        for case in data:
            if  case.get_result("conclusion") not in ["unCrawl"]:
                continue
            ip = case.get_data("ip")
            if "ip" not in ip or ip["ip"] != "yes":
                case.set_result("conclusion","noIP")
                case.set_result("reason","cc_noip")
                case.close = True
