# -*- coding: utf-8 -*-
import sys
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading

import subprocess 
import os 
class Component(_threading.Thread):
    """docstring for BaseData"""
    name = "component"
    cmd = []
    def __init__(self, arg,data):
        super(Component, self).__init__()
        self.settings = arg
        self.cases = data
        self.map = {}

        
        jobdir = self.settings["JOBDIR"]
        workdir = os.path.join(jobdir,self.name)
        if not os.path.exists(workdir):
            os.makedirs(workdir)
        self.in_file = os.path.join(workdir,"in")
        self.out_file = os.path.join(workdir,"out")
        self.err_file = os.path.join(workdir,"err")

    def dump_case(self):
        inf =  open(self.in_file,"w")
        for case in self.cases:
            inf.write(case.target+"\n")
            self.map[case.target] = case
            for cc in case.commons():
                inf.write(cc.target+"\n")
        inf.close()

    def _set_data(self,url,name,data):
        for case in self.cases:
            if case.target == url:
                case.set_data(name,data)
            for cc in case.commons():
                if cc.target == url:
                    cc.set_data(name,data)

    def _pre_data(self,obj,data):
        pass
        
    def parse(self,fname):
        f = open(fname,"r")
        for line in f.readlines():
            line = line.strip().split("\t")
            obj = line[0].strip()
            data = {}
            for item in line[1:]:
                name,value = item.split(":",1)
                data[name]=value.strip()
                self._pre_data(obj,data)
            self._set_data(obj,self.name,data)
        f.close()


    def _run_cmd(self):
        self._stdin = open(self.in_file,"r")
        self._stdout = open(self.out_file,"w")
        self._stderr = open(self.err_file,"w")
        subprocess.call(self.cmd,stderr=self._stderr,stdout=self._stdout,stdin=self._stdin,shell=True)
        self._stdin.close()
        self._stderr.close()
        self._stdout.close()

    def run(self):
        print "[Component:%s] start" %self.name
        if self.settings.getbool("RESUM") == False: 
            self.dump_case()
            self._run_cmd()
        self.parse(self.out_file)
        print "[Component:%s] finished" %self.name



        pass
        
