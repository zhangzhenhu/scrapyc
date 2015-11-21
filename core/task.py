# encoding=utf8
from datetime import datetime
import subprocess
import random
import os, sys
import threading
import Queue
import time
import logging
import os
import socket
from scrapyc_contrib.spider import rpc_control


def get_valid_port(start=8000, end=9000):
    def IsNotOpen(ip="127.0.0.1", port=0):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, int(port)))
            s.shutdown(2)
            return False
        except:
            return True

    for p in range(start, end):
        if IsNotOpen(port=p):
            return p


class Task(threading.Thread):
    """docstring for Task"""

    Running = "Running"
    Failed = "Failed"
    Pending = 'Pending'
    Succeed = 'Succeed'
    Killed = 'Killed'
    Stopping = "Stopping"
    Killing = "Killing"
    Error = "Error"
    Stopped = "Stopped"

    def __init__(self, settings, project, task_config, scrapy_settings, spider_settings, callback=None):
        super(Task, self).__init__()

        # @classmethod
        # def from_crawler(cls,crawler)
        self.settings = settings
        self.project = project
        self.project_name = project.name
        self.project_version = project.version
        self.task_config = task_config
        self.spider_settings = spider_settings
        self.scrapy_settings = scrapy_settings
        self.name = task_config["task_name"]
        self.create_time = datetime.now()
        self.end_time = datetime(1970, 1, 1)
        self.start_time = datetime(1970, 1, 1)

        self.spider = task_config["spider"]
        self.status = Task.Pending
        self.task_id = "%s_%s_%s_%s" % (
            self.project_name, self.spider, self.create_time.strftime("%Y%m%d%H%M%S"), random.randint(1000, 9999))

        self.work_path = os.path.join(task_config["HISTORY_PATH"], self.task_id)
        self.log_path = os.path.join(self.work_path, "log")
        self.data_path = os.path.join(self.work_path, "data")
        self.pid = None
        self.desc = task_config["desc"]
        self.uri = ""
        self.spider_args = ""
        self.retcode = None
        self.runner = os.path.join(os.path.dirname(__file__), "runner.py")

        self.task_env = os.environ.copy()
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
        self.task_env['SCRAPYC_HOME'] = self.settings['HOME_PATH']
        self._stdout = open(os.path.join(self.log_path, "stdout.log"), "w")
        self._stderr = open(os.path.join(self.log_path, "stderr.log"), "w")
        self._p_hander = None
        self._pre_status = None
        self._commands = Queue.Queue()
        self._callback = callback
        self.logger = logging.getLogger("TaskQueue")

        self.default_scrapy_settings = {
            "WEBSERVICE_ENABLED": 1,
            "WEBSERVICE_LOGFILE": str(os.path.join(self.log_path, "webservice.log")),
            "WEBSERVICE_PORT": 0,
            "WEBSERVICE_HOST": "0.0.0.0",
            "LOGSTATS_DUMP_FILE": os.path.join(self.log_path, "stats.log"),
            "JOBDIR": self.data_path,
        }
        self.default_spider_settings = {
            "WORK_PATH": self.work_path,
            "LOG_PATH": self.log_path,
            "DATA_PATH": self.data_path,
        }
        self.task_env['SCRAPY_LOG_FILE'] = str(os.path.join(self.log_path, "scrapy.log"))
        self.webservice_port = 0

        for name, value in self.spider_settings.items():
            self.default_spider_settings[name] = value

        for name, value in self.scrapy_settings.items():
            self.default_scrapy_settings[name] = value

    def _safe(func):
        # print func

        def safe_func(self, *args, **kwargs):
            with self._lock:
                return func(self, *args, **kwargs)

        return safe_func

    def run(self):

        if self.status != self.Pending:
            return
        self.spider_args = ""
        # self.scrapy_args = ""
        self.webservice_port = get_valid_port()
        if not self.webservice_port:
            self.status = Task.Error
            self.logger.error("%s no valid WEBSERVICE_PORT", self.task_id)
            return

        self.default_scrapy_settings["WEBSERVICE_PORT"] = self.webservice_port
        cmdline = [sys.executable, self.runner, "crawl", "--pidfile=%s" % (os.path.join(self.work_path, "pid.log"))]

        for name, value in self.default_scrapy_settings.items():
            # self.scrapy_args += "--set=%s=%s"%(name,value)
            cmdline.append("--set=%s=%s" % (name, value))

        cmdline.append(self.spider)
        for name, value in self.default_spider_settings.items():
            self.spider_args += "-a%s=%s" % (name, value)
            cmdline.append("-a%s=%s" % (name, value))

        self.commands = " ".join(cmdline)
        self.logger.debug("task run %s", self.task_id)
        self.start_time = datetime.now()
        # print self.task_env
        self._p_hander = subprocess.Popen(cmdline, cwd=self.project.source_path, stdin=None, stdout=self._stdout,
                                          stderr=self._stderr, env=self.task_env)

        if not self._p_hander:
            self.status = Task.Error
            self.logger.error("task start error %s", self.task_id)
            return

        self.pid = self._p_hander.pid
        self.status = Task.Running
        self.logger.info("task run pid:%d %s", self.pid, self.task_id)
        while self.retcode == None:
            self.retcode = self._p_hander.poll()
            try:
                cmd_func, args = self._commands.get_nowait()
                cmd_func(args)
            except Queue.Empty, e:
                pass
            except Exception, e:
                self.logger.error("[%s:%d] %s", self.task_id, self.pid, str(e))
            time.sleep(5)
        self.logger.info("[%s:%d] will stop", self.task_id, self.pid)

        self.end_time = datetime.now()
        self._update_status()
        if callable(self._callback):
            self.callback()

    def _update_status(self):

        if self._pre_status == Task.Killing:
            self.status = Task.Killed
        elif self._pre_status == Task.Stopping:
            self.status = Task.Stopped
        elif self.retcode == 0:
            self.status = Task.Succeed
        else:
            self.status = Task.Failed

        self.logger.info("task finished %s %s", self.task_id, self.status)

    def _kill(self, args):

        self._p_hander.kill()
        self._pre_status = Task.Killing

    def kill(self):
        if self.status != Task.Running:
            return
        self.logger.warning("task kill %s" % self.task_id)
        # self._pre_status = Task.Killing
        self._commands.put((self._kill, None))

        # def _stop(self,args):
        # self._pre_status = Task.Stopping
        # return ws.cmd_stop(port=self.webservice_port,spider=self.spider)
        # self._p_hander.terminate()

    def stop(self):
        if self.status != Task.Running:
            return False
        # self._commands.put((self._stop,None))
        self._pre_status = Task.Stopping
        return rpc_control.cmd_stop(port=self.webservice_port, spider=self.spider)

    def is_finished(self):
        if self.status not in [Task.Running, Task.Pending]:
            return True
        else:
            return False

    def to_dict(self):
        if self.status == self.Running:
            run_time = str(datetime.now() - self.start_time)
        else:
            run_time = ""
        return {"task_id": self.task_id,
                "pid": self.pid,
                "task_name": self.name,
                "desc": self.desc,
                "project": self.project_name,
                "version": self.project_version,
                "create_time": self.create_time,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "status": self.status,
                "retcode": self.retcode,
                "log_path": self.log_path,
                "work_path": self.work_path,
                "data_path": self.data_path,
                # "uri":self.uri,
                "spider": self.spider,
                "run_time": run_time,
                # "spider_args":self.spider_args,
                "commands": self.commands,
                "webservice_port": self.webservice_port,

                }


if __name__ == "__main__":
    from project import Project
    from config import Config
    from pprint import pprint
    import pdb

    # pdb.set_trace()
    cfg_file = "C:\\Python27\\Lib\\site-packages\\scrapyc\\server\\projects\\nimei\\scrapy.cfg"
    cfg_config = Config(cfg_file)
    p = Project.from_cfg(cfg_config)
    print "[Project]"
    pprint(p.to_dict())
    print "[Task]"
    task_config = {"HISTORY_PATH": "C:\\Python27\\Lib\\site-packages\\scrapyc\\server\\history",
                   "task_name": "test_task",
                   "run_spider": p.spiders[0],
                   "desc": "desc"}
    spider_params = {}
    t = Task(p, task_config, spider_params)
    t.start()

    # t.wait()
    pprint(t.to_dict())
    import time

    c = 1
    while c < 4:
        print "%s is Running : %s" % (t.task_id, t.isAlive())
        time.sleep(10)
        c += 1

    t.kill()
    t.join()
    pprint(t.to_dict())
    # import pdb
    # pdb.set_trace()
