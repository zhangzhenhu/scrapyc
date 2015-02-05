# -*- coding: utf-8 -*-
from .strategy import Strategy


class Robots(Strategy):
    """docstring for Robots"""
    def run(self,data):
        for case in data:
            if case.close:
                continue
            robots = case.get_data("robots")
            if  not robots or robots.get('robots') != "DISALLOW":
                return
            case.set_result("conclusion","robots")
            case.set_result("reason","robots=DISALLOW")
            case.close = True
        return                