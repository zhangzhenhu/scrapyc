from .strategy import Strategy


class CCDB(Strategy):
    """docstring for CCDB"""
    def __init__(self, arg):
        super(CCDB, self).__init__()
        self.arg = arg

    def run(self,data):

        for case in data:
            if ld.close:
                continue
            ccdb = case.get_date("ccdb")
            if  ccdb["ACK"] != "OK":
                continue

            weight = int(ccdb.get("weight"))
            wise = int(ccdb.get("Wise"))
            flag = ccdb.get("flag")
            #weight = ccdb.get("weight")
            if weight <=10 and weight != 9:
                case.set_result("conclusion","low-weight")
                case.set_result("reason","weight=%d"%weight)
                case.close = True
                continue
            elif flag == "MARKDEL":
                case.set_result("conclusion","markdel")
                case.set_result("reason","flag=%s"%flag)
                case.close = True
                continue
            else:

                case.set_result("conclusion","noproblem")
                case.set_result("reason","wise=%d&&weight=%d&&flag=%s"%(wise,weight,flag)
                case.close = True
                continue


        pass