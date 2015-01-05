# -*- coding: utf-8 -*-
from .component import Component



class LevelSelect(Component):
    """docstring for LevelSelect"""


    name = "level_select"
    cmd = "sh -x ./tools/select/get_prefixt_stat_intps.sh level_select"

    def dump_case(self):
        inf =  open(self.in_file,"w")
        sites = {}
        for case in self.cases:
            sites[case.site] = None
        for site in sites:
            inf.write(site+"\n")
            
        inf.close()
    def parse(self,fname):
        f = open(fname,"r")
        D = {}
        for line in f.readlines():
            line = line.strip().split("\t")
            obj = line[0].strip()
            data = {}
            for item in line[1:]:
                name,value = item.split(":",1)
                data[name]=value.strip()
            D[obj] = data

        f.close()
        for case in self.cases:        
            data = D.get(case.site)
            if data:
                case.set_site_data(self.name,data)

                