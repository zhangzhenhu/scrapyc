# -*- coding: utf-8 -*-
from .strategy import Strategy


class Select(Strategy):
    """docstring for Select"""
    name = "select"

    def stat_level(self,level_data):
        ret = 0
        for key in ["get35","get36","get0"]:
            if key not in level_data:
                continue
            v = level_data[key]
            try:
                ret += int(v)
            except Exception, e:
                ret += 0
        return ret

    def run(self,data):

        for case in data:
            if case.close or case.result.get("conclusion") != "unCrawl":
                continue
            level_all = case.get_site_data("level_all")
            level_select = case.get_site_data("level_select")
            if not level_all:
                continue
            _all = self.stat_level(level_all)
            if not _all :
                continue
            if not level_select:
                continue
            _select = self.stat_level(level_select)
            if _select == 0 or _all /_select >30:
                case.set_result("conclusion","lowFlow")
                case.set_result("reason","can't crawl dealt with in 30 days")
                if _select >0:
                    case.set_result("basis","level_all(high level):%d / level_select(high level):%d = %d"%(_all,_level,_all/_level))
                else:
                    case.set_result("basis","level_all(high level):%d && level_select(high level):0" %(_all))

                case.close = True
                continue
            