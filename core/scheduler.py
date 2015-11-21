# -*- coding: utf-8 -*-
"""


Authors: acmtiger@gmail.com
Date:    2015/11/16 9:42
"""
import os
from core.queue import ProjectQueue, HistoryQueue, TaskQueue
from core.task import Task
import logging


class Scheduler(object):
    """
    核心调度管理器
    分为三个队列：spider项目队列(ProjectQueue)、运行任务管理队列(TaskQueue)、任务历史记录队列(HistoryQueue)
    spider项目队列：
        扫描project目录，从每个spider项目下的scrapy.cfg文件加载项目信息，并进行管理
    运行任务管理队列：
        响应执行任务的请求，启动并管理正在运行的任务，任务结束后移交到HistoryQueue
    HistoryQueue:
        用sqlite数据库实现，记录历史任务记录
    """

    def __init__(self, settings):
        super(Scheduler, self).__init__()
        # 全局配置
        self.settings = settings
        # 注意三个队列的实例化顺序，不能改变
        self.history_queue = HistoryQueue(settings)
        self.project_queue = ProjectQueue(settings)
        self.task_queue = TaskQueue(settings)

        # 初始化logger
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
        """
        启动一个任务
        根据参数创建一个Task对象，并丢给TaskQueue
        Args:
            project_name: spider项目的名称
            spider_name: spider名字
            task_name: 任务名称
            srcapy_config: scapy全局参数（通过-s传入的参数）
            spider_config: spider的参数（通过-a传入的参数）

        Returns:
            bool: 是否成功，这里只能代表是否创建任务成功，无法代表任务是否启动成功，因为任务的启动是TaskQueue管理的
            msg: 错误提示信息

        """
        project, error_msg = self.project_queue.get(project_name)
        if not project:
            return False, error_msg
        task_config = {
            "task_name": task_name,
            "spider": spider_name,
            "desc": "",
            "HISTORY_PATH": self.settings["HISTORY_PATH"],
        }

        task = Task(self.settings, project, task_config, srcapy_config, spider_config)
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
