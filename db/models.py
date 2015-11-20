# encoding=utf8
from sqlalchemy import Column, Integer, String, Enum, Sequence, DateTime
from datetime import datetime
import os
import cPickle as pickle
from db.database import Base


class TaskModel(Base):
    """docstring for Task"""
    __tablename__ = "task"
    id = Column(Integer, Sequence('task_id_seq'), primary_key=True)
    task_id = Column(String(1060), unique=True)
    name = Column(String(1024))
    desc = Column(String(4096))
    project_name = Column(String(1024))
    project_version = Column(String(50))
    spider = Column(String(1024))
    commands = Column(String(4096))
    create_time = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String(20))
    retcode = Column(Integer)
    work_path = Column(String(4096))
    log_path = Column(String(4096))
    data_path = Column(String(4096))
    # uri = Column(String(4096))
    spider_config = Column(String(40960))

    @classmethod
    def from_task(cls, task):
        tm = cls()
        tm.task_id = task.task_id
        tm.name = task.name
        tm.desc = task.desc
        tm.project_name = task.project_name
        tm.project_version = task.project_version
        tm.commands = task.commands
        tm.create_time = task.create_time
        tm.start_time = task.start_time
        tm.end_time = task.end_time
        tm.status = task.status
        tm.retcode = task.retcode
        tm.work_path = task.work_path
        tm.log_path = task.log_path
        tm.data_path = task.data_path
        tm.spider_config = str(task.spider_settings)
        return tm

    def stats(self):
        if self.log_path:
            fd = os.path.join(self.log_path, 'stats.log')
            if not os.path.exists(fd):
                return {}
            with open(fd, 'rb') as f:
                stats = pickle.load(f)
            return stats

    def to_dict(self):

        return {
            "task_id": self.task_id,
            "task_name": self.name,
            "spider": self.spider,
            "desc": self.desc,
            "project": self.project_name,
            "version": self.project_version,
            "commands": self.commands,
            "create_time": self.create_time,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status,
            "retcode ": self.retcode,
            "log_path": self.log_path,
            "work_path": self.work_path,
            "data_path": self.data_path,
            "spider_config": self.spider_config,

        }
