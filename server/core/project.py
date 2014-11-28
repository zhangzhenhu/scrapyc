import os
import imp
import sys
import threading
from scrapy.utils.misc import walk_modules,load_object
from scrapy.utils.spider import iter_spider_classes
from datetime import datetime

class Project(object):


    def __init__(self, cfg_config):
        super(Project, self).__init__()
        self._cfg_confg=cfg_config
        self.name = cfg_config.get("project")
        self.source_path = cfg_config.get("source_path")
        self.author = cfg_config.get("author","")
        self.version = cfg_config.get("version","")
        self.latest_update = datetime.now()
        self.project_setting_module = self._cfg_confg.get("default",None,"settings")
        self.spiders = []
        
        
        #self.spiders = cfg_config.get("spiders","")


    @classmethod
    def from_cfg(cls,cfg_config):
        project = cfg_config.get("project",None)
        if not project:
            return None,"Not found setting : project = {project_name} "
        #print "[project] %s" % project
        p = cls(cfg_config)
        p.load_spiders()
        return p,""


    def load_spiders(self):
        
        sys.path.append(self.source_path)
        try: 
                #sm = import_module("csdn.settings")
            self.spider_modules = load_object(self.project_setting_module +".SPIDER_MODULES")
          
            for name in self.spider_modules:
                for module in walk_modules(name):
                    self._load_spiders(module)
        finally:
            del sys.path[-1]

            #sm = imp.find_module(self.project_setting_module,self.source_path)
    def _load_spiders(self, module):
        for spcls in iter_spider_classes(module):
            self.spiders.append(spcls.name)




    def __repr__(self):
        return "project: %s author: %s version: %s latest_update: %s"  % (
                             self.name, self.author, self.version,self.latest_update)
    def to_dict(self):
        return {"project_name":self.name,
        "source_path":self.source_path,
        "spiders":self.spiders,
        "spider_modules":self.spider_modules,
        "author":self.author,
        "version":self.version,
        "latest_update":self.latest_update,
        "setting_module":self.project_setting_module,
        }


if __name__ == "__main__":
    from config import Config
    cfg_file = "C:\\Python27\\Lib\\site-packages\\scrapyc\\server\\projects\\csdn\\scrapy.cfg"
    cfg_config = Config(cfg_file)
    c = Project.from_cfg(cfg_config)
    print c.to_dict()