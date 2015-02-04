# -*- coding: utf-8 -*-
from .strategy import Strategy


class Common(Strategy):
    """docstring for Common"""


    def run(self,data):
        for case in data:
            if case.close:
                continue
            for cc in case.commons():
                self.wiseccdb(case,cc)
                if not case.close:
                    self.pcccb(case,cc)

    def wiseccdb(self,case,cc):
        ccdb = cc.get_data("wiseccdb")
        if not ccdb or ccdb.get('Last-mod-time')  == "-" or ccdb.get("Weight") == "-":
            return
        weight = int(ccdb.get("Weight"))
        wise = int(ccdb.get("Wise"))
        flag = ccdb.get("Flag")            
        if weight <=10 and weight != 9:
            # case.set_result("conclusion","lowWeight")
            # case.set_result("reason","weight=%d"%weight)
            # case.close = True
            return
        elif flag == "MARKDEL":
            # case.set_result("conclusion","markDel")
            # case.set_result("reason","flag=%s"%flag)
            # case.close = True
            return
        else:

            case.set_result("conclusion","CommonResourceOK")
            case.set_result("reason","commonResource=%s&&wise=%d&&weight=%d&&flag=%s&&ccdb=wise"%(cc.target,wise,weight,flag))
            case.close = True
            case.ok = True
            case.target = cc.target
            return

    def pcccb(self,case,cc):
        ccdb = cc.get_data("pcccdb")
        if  ccdb.get('Last-mod-time')  == "-" or ccdb.get("Weight") == "-":
            return

        weight = int(ccdb.get("Weight"))
        wise = int(ccdb.get("Wise"))
        flag = ccdb.get("Flag")
        #weight = ccdb.get("weight")
        if weight <=10 and weight != 9:
            # case.set_result("conclusion","lowWeight")
            # case.set_result("reason","weight=%d"%weight)
            # case.close = True
            return
        elif flag == "MARKDEL":
            # case.set_result("conclusion","markDel")
            # case.set_result("reason","flag=%s"%flag)
            # case.close = True
            return
        else:

            case.set_result("conclusion","CommonResourceOK")
            case.set_result("reason","commonResource=%s&&wise=%d&&weight=%d&&flag=%s&&ccdb=pc"%(cc.target,wise,weight,flag))
            case.close = True
            case.ok = True
            case.target = cc.target
            return
