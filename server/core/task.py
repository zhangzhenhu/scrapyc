#encoding=utf8
from datetime import datetime
import subprocess
import random
import os,sys
import threading
import Queue
import time
import logging

class Task(threading.Thread):
    """docstring for Task"""

    Running ="Running"
    Failed = "Failed"
    Pending = 'Pending'
    Succeed = 'Succeed'
    Killed = 'Killed'
    Stopping = "Stopping"
    Killing = "Killing"
    Error = "Error"

    def __init__(self, project,task_config,spider_params,callback=None):
        super(Task, self).__init__()

    #@classmethod
    #def from_crawler(cls,crawler)
        self.project = project
        self.project_name = project.name
        self.project_version = project.version
        self.task_config = task_config
        self.spider_params = spider_params
        self.name = task_config["task_name"]
        self.create_time = datetime.now()
        self.end_time = datetime(1970,1,1)
        self.start_time = datetime(1970,1,1)

        self.status = Task.Pending
        self.task_id = "%s_%s_%s"%(self.project_name,self.create_time.strftime("%Y%m%d%H%M%S"),random.randint(100000,999999))
       
        self.work_path = os.path.join(task_config["HISTORY_PATH"],self.task_id)
        self.log_path = os.path.join(self.work_path,"logs")
        self.data_path = os.path.join(self.work_path,"data")
        self.spider = task_config["spider"]
        self.pid= None
        self.desc = task_config["desc"]
        self.uri = ""
        self.spider_config = ""
        self.retcode = None
        self.runner = os.path.join(os.path.dirname(__file__),"runner.py")

        self.task_env = os.environ.copy()
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        self.task_env['SCRAPY_LOG_FILE'] = os.path.join(self.log_path,"scrapy.log")
        #self.task_env['SCRAPY_LOG_FILE'] =
        self._stdout = open(os.path.join(self.log_path,"stdout.log"),"w")
        self._stderr = open(os.path.join(self.log_path,"stderr.log"),"w")
        self._p_hander = None
        self._pre_status = None
        self._commands = Queue.Queue()
        self._callback = callback
        self.logger = logging.getLogger("TaskQueue")
    
    def _safe(func):
        print func
        def safe_func(self,* args, ** kwargs ):
            with self._lock:
                return func( self,*args, **kwargs )
        return safe_func

    def to_dict(self):
        if self.status == self.Running:
            run_time = str(datetime.now() - self.start_time)
        else:
            run_time = ""
        return {"task_id":self.task_id,
            "pid":self.pid,
            "name":self.name,
            "desc":self.desc,
            "project_name":self.project_name,
            "project_version":self.project_version,
            "create_time":self.create_time,
            "start_time":self.start_time,
            "end_time":self.end_time,
            "status":self.status,
            "retcode":self.retcode,
            "log_path":self.log_path,
            "uri":self.uri,
            "spider":self.spider,
            "run_time":run_time,

        }

   
    def run(self):

        if self.status != self.Pending:
            return
        
        args = "-a work_path=%s"%self.work_path
        for name,value in self.spider_params.items():
            args += " -a %s=%s"%(name,value)
        
        self.spider_config = args
            
        cmdline = [sys.executable,self.runner,"crawl",self.spider]
        if args:
            cmdline.append(args)
        self.logger.debug("task run %s %s",self.task_id,cmdline)
        self.start_time =  datetime.now()
        self._p_hander = subprocess.Popen(cmdline,cwd = self.project.source_path,stdin=None, stdout=self._stdout, stderr=self._stderr,env=self.task_env)

        if not self._p_hander:
            self.status = Task.Error
            self.logger.error("task start error %s",self.task_id)
            return
        
        self.pid = self._p_hander.pid
        self.status = Task.Running
        self.logger.info("task run pid:%d %s",self.pid,self.task_id)
        while self.retcode == None:
            self.retcode = self._p_hander.poll()
            try:
                cmd_func,args = self._commands.get_nowait()
                cmd_func(args)
            except  Queue.Empty, e:
                pass
            time.sleep(5)
        self.end_time = datetime.now()
        self._update_status()
        if callable(self._callback):
            self.callback()

    def _update_status(self):

        if self._pre_status == Task.Killing:
            self.status = Task.Killed
        elif self._pre_status == Task.Stopping:
            self.status = Task.Stoped
        elif self.retcode == 0:
            self.status = Task.Succeed
        else:
            self.status = Task.Failed
       
        self.logger.info("task finished %s %s",self.task_id,self.status)
    def _kill(self,args):
        
        self._p_hander.kill()
        self._pre_status = Task.Killing

    def kill(self):
        if self.status != Task.Running:
            return
        self.logger.warning("task kill %s"%self.task_id)
        #self._pre_status = Task.Killing
        self._commands.put((self._kill,None))

    def _stop(self,args):
        self._p_hander.terminate()
        self._pre_status = Task.Stopping

    def stop(self):
        if self.status != Task.Running:
            return
        self._commands.put((self._stop,None))


    def is_finished(self):
        if self.status not in [Task.Running,Task.Pending]:
            return True
        else:
            return  False



if __name__ == "__main__":
    from project import Project
    from config import Config
    from pprint import pprint
    import pdb
    #pdb.set_trace()
    cfg_file = "C:\\Python27\\Lib\\site-packages\\scrapyc\\server\\projects\\nimei\\scrapy.cfg"
    cfg_config = Config(cfg_file)
    p = Project.from_cfg(cfg_config)
    print "[Project]"
    pprint( p.to_dict())
    print "[Task]"
    task_config = {"HISTORY_PATH":"C:\\Python27\\Lib\\site-packages\\scrapyc\\server\\history",
    "task_name":"test_task",
    "run_spider":p.spiders[0],
    "desc":"desc"}
    spider_params = {}
    t = Task(p,task_config,spider_params)
    t.start()

    #t.wait()
    pprint(t.to_dict())
    import time
    c=1
    while  c < 4:
        print "%s is Running : %s"%(t.task_id,t.isAlive())
        time.sleep(10)
        c += 1
    
    t.kill()
    t.join()
    pprint(t.to_dict())
    #import pdb
    #pdb.set_trace()