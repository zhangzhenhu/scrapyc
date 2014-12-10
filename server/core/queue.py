#encoding=utf8
from sqlalchemy.orm.exc import NoResultFound
from scrapyc.server.core.project import Project
from scrapyc.server.core.config import Config
#from scrapyc.server.core.database import SafeSession
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
        #session = settings["db_session"]
        self.settings.set("project_queue",self)

        self.logger = logging.getLogger("ProjectQueue")
        log_file = os.path.join(settings.get("LOG_PATH"),"project_queue.log")
        handler=logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter(self.settings.get("LOG_FORMATER")))
        handler.setLevel(self.settings.get("LOG_LEVEL",logging.INFO))
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
            return self._queue[project_name],""   
        return None,"%s not exists" %project_name

    def start(self):
        pass
    def stop(self):
        pass

from scrapyc.server.core.models import TaskModel
from scrapyc.server.core.database import  SafeSession
class HistoryQueue(object):
    """docstring for TaskDB"""
    def __init__(self, settings):
        super(HistoryQueue, self).__init__()
        self.settings = settings
        self.settings.set("history_queue",self)
        #session = db_session#settings["db_session"]

        self.logger = logging.getLogger("HistoryQueue")
        log_file = os.path.join(settings.get("LOG_PATH"),"history_queue.log")
        handler=logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter(self.settings.get("LOG_FORMATER")))
        handler.setLevel(self.settings.get("LOG_LEVEL",logging.INFO))        
        self.logger.addHandler(handler)


    def count(self):       
        session = SafeSession()
        r =session.query(TaskModel).count()        
        SafeSession.remove()
        return r

    def all(self):
        session = SafeSession()
        r =  session.query(TaskModel).order_by(TaskModel.end_time.desc())
        SafeSession.remove()
        return r

    def page(self,index=1,page_count=10):
        session = SafeSession()
        if index<1:index=1
        total_count = session.query(TaskModel).count()
        total_page = (total_count+page_count-1)/page_count 
        if index>total_page:index = total_page
        r =  session.query(TaskModel).order_by(TaskModel.end_time.desc()).offset( (index -1)*page_count).limit(page_count)
        SafeSession.remove()
        
        return r,index,total_page,page_count,total_count

    def get(self,task_id):
        try:
            session = SafeSession()
            r= session.query(TaskModel).filter_by(task_id=task_id).one()
            SafeSession.remove()
        except NoResultFound, e:
            r = None
       
        return r

    
    def remove_by_taskid(self,task_id):
        if not task_id or not  isinstance(str,task_id):
            return
        session = SafeSession()
        for task in session.query(TaskModel).filter_by(task_id=task_id).all():
            session.delete(task)
        SafeSession.remove()
        
        
       

    def remove_by_project(self,project_name):

        if not project_name or not  isinstance(str,project_name):
            return
        session = SafeSession()
        for task in session.query(TaskModel).filter_by(project_name=project).all():
            session.delete(task)
        SafeSession.remove()
        
        
       
   
    def put(self,task):

        tm = TaskModel.from_task(task)
        if tm:
            session = SafeSession()
            session.add(tm)  
            session.commit()
            SafeSession.remove()
        else:
            self.logger.error("init TaskModel object error %s",task.task_id )

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
        self._max_proc = self.settings.get("MAX_RUN_TASK",10)

        self.logger = logging.getLogger("TaskQueue")
        log_file = os.path.join(self.settings.get("LOG_PATH"),"task_queue.log")
        handler=logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter(self.settings.get("LOG_FORMATER")))
        handler.setLevel(self.settings.get("LOG_LEVEL",logging.INFO))        
        self.logger.addHandler(handler)

        self._pending_queue = Queue.Queue()
        self._running_queue = {}
        self._lock = threading.RLock()
            
    def _do_pending(self):

        if len(self._running_queue) >= self._max_proc:
            self.logger.debug("max running task %d",self._max_proc)
            return
        try:
            task = self._pending_queue.get_nowait()
        except Queue.Empty, e:
            return
            pass 
        if task:
            with self._lock:
                self.logger.debug("put running queue %s",task.task_id)
                self._running_queue[task.task_id] = task
            task.start()
        
    def _do_finished(self):
        with self._lock:
            for task in self._running_queue.values():
                if not task.is_finished():
                    self.logger.debug("status check %s %s",task.task_id,task.status)
                    continue
                self.logger.debug("put history_queue %s",task.task_id)
                self._history_queue.put(task)
                del self._running_queue[task.task_id]

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
        self.logger.debug("put task to pending_queue %s %s %s ",task.task_id,task.project_name,task.spider)
        return True  
    
    def kill_task(self,task_id):
        if task_id not in self._running_queue:
            self.logger.warning("task not found %s",task_id)
            return False,"task_id:%s Not found"%task_id

        self.logger.debug("killing task  %s",task_id)

        with self._lock:    
            self._running_queue[task_id].kill()
        return True,"success"
        
    def stop_task(self,task_id):
        if task_id not in self._running_queue:
            self.logger.warning("task not found %s",task_id)
            return False,"task_id:%s Not found"%task_id

        self.logger.debug("killing task  %s",task_id)

        with self._lock:    
            self._running_queue[task_id].stop()
        return True,"success"

    def kill_all(self):
        self.logger.warning("kill all task...")
        with self._lock:
            for task in self._running_queue.values():
                task.kill()

    def all(self):        
        return self._running_queue.values()

    def count(self):
        return len(self._running_queue)
