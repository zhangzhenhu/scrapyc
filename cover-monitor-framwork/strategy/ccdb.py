from .strategy import Strategy


class CCDB(Strategy):
    """docstring for CCDB"""


    def run(self,data):
        for case in data:
            if case.close:
                continue
            self.wiseccdb(case)
            if not case.close:
                self.pcccb(case)

    def wiseccdb(self,case):
        ccdb = case.get_data("wiseccdb")
        if  ccdb["Last-mod-time"]  == "-":
            return
        weight = int(ccdb.get("Weight"))
        wise = int(ccdb.get("Wise"))
        flag = ccdb.get("Flag")            
        if weight <=10 and weight != 9:
            case.set_result("conclusion","low-weight")
            case.set_result("reason","weight=%d"%weight)
            case.close = True
            return
        elif flag == "MARKDEL":
            case.set_result("conclusion","markdel")
            case.set_result("reason","flag=%s"%flag)
            case.close = True
            return
        else:

            case.set_result("conclusion","noproblem")
            case.set_result("reason","wise=%d&&weight=%d&&flag=%s"%(wise,weight,flag))
            case.close = True
            return

    def pcccb(self,case):
        ccdb = case.get_data("pcccdb")
        if  ccdb["Last-mod-time"]  == "-":
            return

        weight = int(ccdb.get("Weight"))
        wise = int(ccdb.get("Wise"))
        flag = ccdb.get("Flag")
        #weight = ccdb.get("weight")
        if weight <=10 and weight != 9:
            case.set_result("conclusion","low-weight")
            case.set_result("reason","weight=%d"%weight)
            case.close = True
            return
        elif flag == "MARKDEL":
            case.set_result("conclusion","markdel")
            case.set_result("reason","flag=%s"%flag)
            case.close = True
            return
        else:

            case.set_result("conclusion","noproblem")
            case.set_result("reason","wise=%d&&weight=%d&&flag=%s"%(wise,weight,flag))
            case.close = True
            return
