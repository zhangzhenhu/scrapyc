# -*- coding: utf-8 -*-
"""


Authors: acmtiger@gmail.com
Date:    2015/11/16 9:42
"""
import os
import logging
import threading
import time
import Queue
from sqlalchemy.orm.exc import NoResultFound
from core.project import Project
from core.config import Config
from db.models import TaskModel
from db.database import SafeSession
import traceback


class ProjectQueue(object):
    """
    管理项目的队列
    """

    def __init__(self, settings):
        super(ProjectQueue, self).__init__()
        self.settings = settings
        # session = settings["db_session"]
        self.settings["project_queue"] = self

        self.logger = logging.getLogger("ProjectQueue")
        log_file = os.path.join(settings.get("LOG_PATH"), "project_queue.log")
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter(self.settings.get("LOG_FORMATER")))
        handler.setLevel(self.settings.get("LOG_LEVEL", logging.INFO))
        self.logger.addHandler(handler)

        self._queue = {}

    def reload(self):
        """
        扫描project目录，加载spider项目
        Returns:

        """
        projects_path = self.settings.get("PROJECT_PATH")
        error_msg = ""
        self._queue = {}
        # session = self.db_engine.session()
        if not os.path.exists(projects_path):
            self.logger.error("project path not exists : %s" % projects_path)
            return False

        for pro in os.listdir(projects_path):
            cfg_file = os.path.join(projects_path, pro, "scrapy.cfg")
            if not os.path.exists(cfg_file):
                self.logger.warning("project config file not found : %s" % (cfg_file))
                continue

            cfg_config = Config(cfg_file)
            try:
                p, error_msg = Project.from_cfg(cfg_config)
                if not p:
                    self.logger.error("Project init from cfg failed. %s : %s", error_msg, cfg_config)
                    continue
            except:
                self.logger.error(traceback.format_exc())
                continue
            self._queue[p.name] = p
        return len(self._queue)

    def count(self):
        return len(self._queue)

    def all(self):
        return self._queue.values()

    def get(self, project_name):
        if project_name in self._queue:
            return self._queue[project_name], ""
        return None, "%s not exists" % project_name

    def start(self):
        pass

    def stop(self):
        pass


class HistoryQueue(object):
    """
    管理任务历史的队列，数据存储在sqlite数据库中
    """

    def __init__(self, settings):
        super(HistoryQueue, self).__init__()
        self.settings = settings
        self.settings["history_queue"] = self
        # session = db_session#settings["db_session"]

        self.logger = logging.getLogger("HistoryQueue")
        log_file = os.path.join(settings.get("LOG_PATH"), "history_queue.log")
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter(self.settings.get("LOG_FORMATER")))
        handler.setLevel(self.settings.get("LOG_LEVEL", logging.INFO))
        self.logger.addHandler(handler)

    def count(self):
        """
        统计数据库中有多少条任务历史记录
        Returns: int：记录的数量

        """
        session = SafeSession()
        r = session.query(TaskModel).count()
        SafeSession.remove()
        return r

    def all(self):
        """
        查询返回所有记录
        按照任务的结束时间排序
        Returns: list: 任务历史记录

        """
        session = SafeSession()
        r = session.query(TaskModel).order_by(TaskModel.end_time.desc())
        SafeSession.remove()
        return r

    def page(self, index=1, page_count=10):
        """
        查询返回某一页的历史记录
        Args:
            index: int: 起始记录位置
            page_count: int:每一页的数量，亦即返回多少条

        Returns:
            list:r:查询结果
            int:index:起始位置
            int:total_page： 一共多少页
            int:page_count: 每一页的数量
            int:total_count: 一共的记录数

        """
        session = SafeSession()
        if index < 1:
            index = 1
        # 一共的记录数
        total_count = session.query(TaskModel).count()
        # 一共有多少页
        total_page = (total_count + page_count - 1) / page_count
        if index > total_page:
            index = total_page
        r = session.query(TaskModel).order_by(TaskModel.end_time.desc()).offset((index - 1) * page_count).limit(
            page_count)
        SafeSession.remove()

        return r, index, total_page, page_count, total_count

    def get(self, task_id):
        """
        查询某一个特定任务
        Args:
            task_id: str:要查询的任务id

        Returns:
            list: 查询结果
        """
        try:
            session = SafeSession()
            r = session.query(TaskModel).filter_by(task_id=task_id).one()
            SafeSession.remove()
        except NoResultFound, e:
            r = None

        return r

    def remove_by_taskid(self, task_id):
        """
        删除某一个任务
        Args:
            task_id: str:任务id

        Returns:

        """
        if not task_id or not isinstance(str, task_id):
            return
        session = SafeSession()
        for task in session.query(TaskModel).filter_by(task_id=task_id).all():
            session.delete(task)
        SafeSession.remove()

    def remove_by_project(self, project_name):
        """
        删除某个项目的所有历史记录
        Args:
            project_name: str:项目名称

        Returns:

        """
        if not project_name or not isinstance(str, project_name):
            return
        session = SafeSession()
        for task in session.query(TaskModel).filter_by(project_name=project).all():
            session.delete(task)
        SafeSession.remove()

    def put(self, task):

        tm = TaskModel.from_task(task)
        if tm:
            session = SafeSession()
            session.add(tm)
            session.commit()
            SafeSession.remove()
        else:
            self.logger.error("init TaskModel object error %s", task.task_id)

    def start(self):
        pass

    def stop(self):
        pass


class TaskQueue(threading.Thread):
    """
    管理正在调度的任务队列
    用子线程的方式实现
    """

    def __init__(self, settings):
        super(TaskQueue, self).__init__()
        self.settings = settings
        self.settings["task_queue"] = self
        self._history_queue = self.settings["history_queue"]
        self._max_proc = self.settings.get("MAX_RUN_TASK", 10)

        self.logger = logging.getLogger("TaskQueue")
        log_file = os.path.join(self.settings.get("LOG_PATH"), "task_queue.log")
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter(self.settings.get("LOG_FORMATER")))
        handler.setLevel(self.settings.get("LOG_LEVEL", logging.INFO))
        self.logger.addHandler(handler)

        self._pending_queue = Queue.Queue()
        self._running_queue = {}
        self._lock = threading.RLock()

    def _do_pending(self):
        """
        从等待队列中取出一个任务启动，并移到正在运行队列
        Returns:

        """
        if len(self._running_queue) >= self._max_proc:
            self.logger.debug("max running task %d", self._max_proc)
            return
        try:
            task = self._pending_queue.get_nowait()
        except Queue.Empty, e:
            return
            pass
        if task:
            with self._lock:
                self.logger.debug("put running queue %s", task.task_id)
                self._running_queue[task.task_id] = task
            task.start()

    def _do_finished(self):
        """
        扫描正在运行的队列，把已经结束的任务移到历史队列中
        Returns:

        """
        with self._lock:
            for task in self._running_queue.values():
                if not task.is_finished():
                    self.logger.debug("status check %s %s", task.task_id, task.status)
                    continue
                self.logger.debug("put history_queue %s", task.task_id)
                self._history_queue.put(task)
                del self._running_queue[task.task_id]

    def run(self):
        """
        线程执行过程
        Returns:

        """
        self.logger.info("start")
        self._keeping = True
        while self._keeping:
            self._do_pending()
            self._do_finished()
            time.sleep(5)

    def stop(self):
        """
        停止队列
        Returns:

        """
        self.logger.warning("stopping..")
        self.kill_all()
        while len(self._running_queue) > 0:
            time.sleep(5)
        self._keeping = False
        self.join()

    def put(self, task):
        """
        加入一个新任务，先加入到等待队列中
        本方法是外部调用的接口
        Args:
            task:

        Returns:

        """
        self._pending_queue.put(task)
        self.logger.debug("put task to pending_queue %s %s %s ", task.task_id, task.project_name, task.spider)
        return True

    def kill_task(self, task_id):
        """
        强制杀死一个任务的进程

        Args:
            task_id: str:任务id

        Returns:

        """
        if task_id not in self._running_queue:
            self.logger.warning("task not found %s", task_id)
            return False, "task_id:%s Not found" % task_id

        self.logger.debug("killing task  %s", task_id)

        with self._lock:
            self._running_queue[task_id].kill()
        return True, "success"

    def stop_task(self, task_id):
        """
        停止一个任务
        通过rpc的方式给spider进程发送一个stop命令
        Args:
            task_id:

        Returns:

        """
        if task_id not in self._running_queue:
            self.logger.warning("task not found %s", task_id)
            return False, "task_id:%s Not found" % task_id

        self.logger.debug("killing task  %s", task_id)

        with self._lock:
            self._running_queue[task_id].stop()
        return True, "success"

    def kill_all(self):
        """
        强制杀死所有任务的进程
        Returns:

        """
        self.logger.warning("kill all task...")
        with self._lock:
            for task in self._running_queue.values():
                task.kill()

    def all(self):
        """
        返回所有正在执行任务的task对象
        Returns:
            int:数量
        """
        return self._running_queue.values()

    def count(self):
        """
        返回正在运行任务的数量
        Returns:
            int:数量
        """
        return len(self._running_queue)

    def get_task(self, task_id):
        """
        查询一个任务的task对象
        Args:
            task_id: str:任务的id

        Returns:
            Task:任务的task对象
        """
        if task_id in self._running_queue:
            return self._running_queue[task_id]
        else:
            return None
