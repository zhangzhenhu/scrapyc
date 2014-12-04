import os
import sys
import logging
from scrapyc.server.core.settings import Settings



class CoreApp(object):
    """docstring for CoreApp"""
    config = Settings()
    scheduler = None
    def __init__(self):
        super(CoreApp, self).__init__()


        #_handler = XMLRPCHandler('api')
        #_scheduler_proxy = SchedulerProxy(app)
        #_handler.register_instance(scheduler_proxy)
        #_handler.connect(app, '/api')    
        #self.scheduler = 
    #def from_other(self):
    def init(self,setting_module=None):
        
        #FORMAT = "%(asctime)s [%(filename)s-%(funcName)s-%(lineno)d] %(levelname)s %(message)s"

        #project_settings = os.environ("SCRAPYC_SETTINGS")
        if setting_module == None:
            setting_module = os.environ["SCRAPYC_SETTINGS"]

        self.config.setmodule(setting_module)
        
        logging.basicConfig(format=self.config.get("LOG_FORMATER"),level=self.config.get("LOG_LEVEL",logging.INFO))
        
        for _path_config in ["LOG_PATH","DATA_PATH","PROJECT_PATH","HISTORY_PATH"]:
            _p = self.config.get(_path_config)
            if not os.path.exists(_p):
                os.mkdir(_p)

        from scrapyc.server.core.scheduler import Scheduler
        self.scheduler = Scheduler(self.config)
        
        #self.scheduler.project_reload()
    def start(self):
        self.scheduler.start()
        
    def stop(self):
        if self.scheduler:
            self.scheduler.stop() 

coreapp = CoreApp()



#app.config.from_object('scrapyc.server.crawler.default_settings')
#app.config.from_envvar('SCRAPYC_SETTINGS',silent=True)




#encoding=utf8
#

#import scrapyc.server.crawler.database
#import scrapyc.server.crawler.views

    




