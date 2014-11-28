#encoding=utf8
import os
#from scrapyc.server.core.config import Config
from scrapyc.server.core.queue import ProjectQueue,HistoryQueue,TaskQueue
from scrapyc.server.core.task import Task
import threading
import logging


class Scheduler(object):
    """docstring for Scheduler"""
    def __init__(self, settings):
        super(Scheduler, self).__init__()
        self.settings = settings
        self.task_queue = TaskQueue(settings)
        self.history_queue = HistoryQueue(settings)
        self.project_queue = ProjectQueue(settings)
        self._lock = threading.Lock()
        self.logger = logging.getLogger("Scheduler")
        log_file = os.path.join(settings.get("LOG_PATH"),"scheduler_queue.log")
        handler=logging.FileHandler(log_file)
        self.logger.addHandler(handler)      
    
    
    def start(self):
        self.logger.info("start...")
        self.history_queue.start()
        self.project_queue.start()
        self.task_queue.start()
        self.logger.info("started ok")
    
    def stop(self):
        self.logger.info("stopping")
        self.history_queue.stop()
        self.project_queue.stop()       
        self.task_queue.stop()
        self.logger.info("stopped")

    def start_job(self,project_name,spider_name,task_params):
        project,error_msg= self.project_queue.get(project_name)
        if not project:
            return False,error_msg
        task_config = {
        "task_name":"test",
        "spider":spider_name,
        "desc":"",
        "HISTORY_PATH":self.settings["HISTORY_PATH"],
        }
        
        task = Task(project,task_config,{})
        self.task_queue.put(task)
        return True,"succed"
        

    def stop_job(self):
        pass

    def kill_job(self):
        pass



    def project_all(self):
        return self.project_queue.all()

    def project_count(self):
        return self.project_queue.count()

    def project_reload(self):
        return self.project_queue.reload()


    def history_all(self):

        return self.history_queue.all()


        