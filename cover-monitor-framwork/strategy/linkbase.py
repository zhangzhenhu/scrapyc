from .strategy import Strategy


class Linkbase(Strategy):
    """docstring for Linkbase"""
    def __init__(self, arg):
        super(Linkbase, self).__init__()
        self.arg = arg

    def run(self,data):

        for case in data:
            if ld.close:
                continue
            ld = case.get_date("linkbase")

            urlnew = ld.get("urlnew")
            if urlnew == "CHK" :
                case.set_result("conclusion","lbdiff")
                case.close = True
                continue
            elif urlnew == "GET":
                case.set_result("conclusion","uncrawl")
                case.close = True
                continue

            l2patch = case.get_date("l2patch")
            if l2patch and l2patch["del_reason"] != "-" :
                case.set_result("conclusion","lbdel")
                case.set_result("reason",l2patch["del_reason"])
                case.close = True
                continue
            l2base = case.get_date("l2base")
            
            if l2base and l2base["del_reason"] != "-" :
                case.set_result("conclusion","lbdel")
                case.set_result("reason",l2base["del_reason"])
                case.close = True
                continue



        pass