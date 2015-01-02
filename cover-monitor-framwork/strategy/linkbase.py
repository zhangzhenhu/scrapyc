from .strategy import Strategy


class Linkbase(Strategy):
    """docstring for Linkbase"""


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
                    case.set_result("conclusion","lbdiff")
                    case.close = True
                    continue
                elif urlnew == "GET":
                    case.set_result("conclusion","uncrawl")
                    case.close = True
                    continue

            if l2patch and l2patch["del_reason"] != "-" :
                case.set_result("conclusion","lbdel")
                case.set_result("reason",l2patch["del_reason"])
                case.close = True
                continue
            
            if l2base and l2base["del_reason"] != "-" :
                case.set_result("conclusion","lbdel")
                case.set_result("reason",l2base["del_reason"])
                case.close = True
                continue



        pass