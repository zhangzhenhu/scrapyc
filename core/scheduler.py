# -*- coding: utf-8 -*-
"""


Authors: acmtiger@gmail.com
Date:    2015/11/16 9:42
"""
import os
# from scrapyc.server.core.config import Config
from core.queue import ProjectQueue, HistoryQueue, TaskQueue
from core.task import Task
import threading
import logging


class Scheduler(object):
    """docstring for Scheduler"""

    def __init__(self, settings):
        super(Scheduler, self).__init__()
        self.settings = settings
        # 注意三个队列的实例化顺序
        self.history_queue = HistoryQueue(settings)
        self.project_queue = ProjectQueue(settings)
        self.task_queue = TaskQueue(settings)

        self._lock = threading.Lock()
        self.logger = logging.getLogger("Scheduler")
        log_file = os.path.join(settings.get("LOG_PATH"), "scheduler_queue.log")
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter(self.settings.get("LOG_FORMATER")))
        handler.setLevel(self.settings.get("LOG_LEVEL", logging.INFO))
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

    def task_start(self, project_name, spider_name, task_name, srcapy_config, spider_config):
        project, error_msg = self.project_queue.get(project_name)
        if not project:
            return False, error_msg
        task_config = {
            "task_name": task_name,
            "spider": spider_name,
            "desc": "",
            "HISTORY_PATH": self.settings["HISTORY_PATH"],
        }

        task = Task(project, task_config, srcapy_config, spider_config)
        self.task_queue.put(task)
        return True, "succed"

    def task_stop(self):
        pass

    def task_all(self):
        return self.task_queue.all()

    def task_count(self):
        return self.task_queue.count()

    def task_kill(self, task_id):
        return self.task_queue.kill_task(task_id)

    def task_stop(self, task_id):
        return self.task_queue.stop_task(task_id)

    def project_all(self):
        return self.project_queue.all()

    def project_count(self):
        return self.project_queue.count()

    def project_reload(self):
        return self.project_queue.reload()

    def project_get(self, project_name):
        return self.project_queue.get(project_name)

    def history_all(self):
        return self.history_queue.all()
