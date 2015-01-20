# -*- coding: utf-8 -*-
from .component import Component



class Linkbase(Component):
    """docstring for Linkbase"""


    name = "linkbase"
    cmd = "sh -x ./tools/linkbase/seekglobal.sh "
    
    def _pre_data(self,obj,data):
      
        if "history" not in  data or not isinstance(data["history"],str) :
            return
        data["crawl_fail"] = False
        data["craw_count"] = 0
        data["fail_count"] = 0              
        hd = data["history"].strip()
        if not hd or hd in ["-","NULL"] or len(hd) < 10:
            return
        ret = []
             
        craw_count = 0 
        fail_count = 0
        for item in hd[1:-1].split("', '"):
            item = item.split(" : ",1)
            ret.append(item)
            if "NOT_USE" == item[0]:
                continue
            craw_count += 1
            if "FAIL" in item[0]:
                fail_count += 1
        if craw_count  and craw_count == fail_count:
            data["crawl_fail"] = True

        data["craw_count"] = craw_count
        data["fail_count"] = fail_count
        data["history"] = ret

        data["crawl_fail"] = True        
