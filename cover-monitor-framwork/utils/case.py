# -*- coding: utf-8 -*-
import threading
from .url import get_url_site

class Case(object):
    """docstring for Case"""
    def __init__(self, arg,line):
        super(Case, self).__init__()
        self.settings = arg
        self.origin = line
        line=line.strip().split("\t")
        self.objurl = line[0]
        self.other=line[1:]
        self.target = self.objurl
        self.common = {}

        self.data = {}
        self.site_data = {}
        self.domain_data = {}
        #self._lock = threading.RLock()
        self.close = False
        self.valid = True
        self.ok = False
        
        self.site = get_url_site(self.objurl)

        self.domain = ""
        self.result = {

        }
        self._result_schema = [       
        "conclusion",
        "reason",
        "basis",
        "additional",
        "solution",
        "owner",
        ]

    def  add_common(self,url):
        if url not in self.common:
            self.common[url] = Case(self.settings,url)
    def commons(self):
        return self.common.values()
    def get_common(self,url):
        if url in self.common:
            return self.common[url]
        return None
        
    def get_data(self,name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def set_data(self,name,value):
        #if self._lock.acquire():
        print "[case] add data %s %s"%(name,self.target)
        self.data[name]=value
        #self._lock.release()

    def get_site_data(self,name):
        if name in self.site_data:
            return self.site_data[name]
        else:
            return None

    def set_site_data(self,name,value):
        #if self._lock.acquire():
        print "[case] add site data %s %s"%(name,self.objurl)
        self.site_data[name]=value

    def get_domain_data(self,name):
        if name in self.domain_data:
            return self.domain_data[name]
        else:
            return None

    def set_domain_data(self,name,value):
        #if self._lock.acquire():
        print "[case] add domain data %s %s"%(name,self.objurl)
        self.domain_data[name]=value




    def set_result(self,name,value):
        if name in self._result_schema:
            self.result[name]=value
            return True
        return False
    



    def __str__(self):
        s = self.objurl + "\t".join(self.other)
        for key in self._result_schema:
            if key in self._result:
                v = self._result[key]
            else:
                v = ""
            s += "\t" + v
        return s


        