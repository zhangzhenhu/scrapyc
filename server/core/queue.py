#encoding=utf8
from sqlalchemy.orm.exc import NoResultFound
from scrapyc.server.core.project import Project
from scrapyc.server.core.config import Config
import os
import logging
import threading
import time
import Queue

class ProjectQueue(object):
    """docstring for ProjectQueue"""
    def __init__(self, settings):
        super(ProjectQueue, self).__init__()
        self.settings = settings
        #self.db_session = settings["db_session"]
        self.settings.set("project_queue",self)

        self.logger = logging.getLogger("ProjectQueue")
        log_file = os.path.join(settings.get("LOG_PATH"),"project_queue.log")
        handler=logging.FileHandler(log_file)
        self.logger.addHandler(handler)

        self._queue = {}

    def reload(self):
        projects_path =self.settings.get("PROJECT_PATH")
        error_msg = ""
        self._queue = {}
        #session = self.db_engine.session()
        if not os.path.exists(projects_path):
            self.logger.error("project path not exists : %s"%projects_path)
            return  False
        
        for pro in os.listdir(projects_path):
            cfg_file = os.path.join(projects_path,pro,"scrapy.cfg")
            if not os.path.exists(cfg_file):
                self.logger.warning("project config file not found : %s"%(cfg_file))
                continue
            
            cfg_config = Config(cfg_file)
            p,error_msg = Project.from_cfg(cfg_config)
            if not p:
                self.logger.error("Project init from cfg failed. %s : %s",error_msg,cfg_config)
                continue
            self._queue[p.name] = p
        return len(self._queue)
                  
    def count(self):
         return len(self._queue)

    def all(self):
        return self._queue.values()

    def get(self,project_name):       
        if project_name in self._queue:
            return self._queue[project_name]       
        return None
    def start(self):
        pass
    def stop(self):
        pass

from scrapyc.server.core.models import TaskModel,db_session
class HistoryQueue(object):
    """docstring for TaskDB"""
    def __init__(self, settings):
        super(HistoryQueue, self).__init__()
        self.settings = settings
        self.settings.set("history_queue",self)
        self.db_session = db_session#settings["db_session"]

        self.logger = logging.getLogger("HistoryQueue")
        log_file = os.path.join(settings.get("LOG_PATH"),"history_queue.log")
        handler=logging.FileHandler(log_file)
        self.logger.addHandler(handler)


    def count(self):       
         r = self.db_session.query(TaskModel).count()        
         self.db_session.remove()
         return r

    def all(self):
    
        r =  self.db_session.query(TaskModel).all()
        self.db_session.remove()
        return r


    def get(self,task_id):
        try:
            r= self.db_session.query(TaskModel).filter_by(task_id=task_id).one()
        except NoResultFound, e:
            r = None
        self.db_session.remove()
        return r

    
    def remove_by_taskid(self,task_id):
        if not task_id or not  isinstance(str,task_id):
            return
        for task in self.db_session.query(TaskModel).filter_by(task_id=task_id).all():
            self.db_session.delete(task)
        
        self.db_session.commit()
        self.db_session.remove()

    def remove_by_project(self,project_name):
        if not project_name or not  isinstance(str,project_name):
            return
        for task in self.db_session.query(TaskModel).filter_by(project_name=project).all():
            self.db_session.delete(task)
        
        self.db_session.commit()
        self.db_session.remove()
   
    def put(self,task):
        tm = TaskModel.from_task(task)
        if tm:
            self.db_session.add(tm)
            self.db_session.commit()
            self.db_session.remove()

    def start(self):
        pass
    def stop(self):
        pass
        
class TaskQueue(threading.Thread):
    """docstring for TaskQueue"""
    def __init__(self, settings):
        super(TaskQueue, self).__init__()
        self.settings = settings
        self.settings.set("task_queue",self)
        self._history_queue = self.settings["history_queue"]
        self._max_proc = self.settings["MAX_RUN_TASK"]

        self.logger = logging.getLogger("TaskQueue")
        log_file = os.path.join(self.settings.get("LOG_PATH"),"task_queue.log")
        handler=logging.FileHandler(log_file)
        self.logger.addHandler(handler)

        self._pending_queue = Queue.Queue()
        self._running_queue = {}
        self._lock = threading.RLock()
            
    def _do_pending(self):

        if len(self._running_queue) >= self._max_proc:
                return
        try:
            task = self._pending_queue.get_nowait()
        except Queue.Empty, e:
            pass 
        if task:
            with self._lock:
                self._running_queue[task.task_id] = task
            task.start()
        
    def _do_finished(self):
        with self._lock:
            for task in self._running_queue.values():
                if task.is_running():
                    continue
                self._history_queue.put(task)

    def run(self):
        self.logger.info("start")
        self._keeping = True
        while self._keeping:
            self._do_pending()
            self._do_finished()
            time.sleep(5)


    def stop(self):
        self.logger.warning("stopping..")
        self.kill_all()
        while len(self._running_queue) >0:
            time.sleep(5)
        self._keeping = False
        self.join()

    def put(self,task):
        self._pending_queue.put(task)
        return True  
    
    def kill_all(self):
        self.logger.warning("kill all task...")
        with self._lock:
            for task in self._running_queue.values():
                task.kill()
