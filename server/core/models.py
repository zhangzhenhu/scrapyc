#encoding=utf8
from sqlalchemy import Column, Integer, String,Enum,Sequence,DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from scrapyc.server.core.database import Base,db_engine,db_session
import os,sys


class TaskModel(Base):
    """docstring for Task"""
    __tablename__ = "task"
    id = Column(Integer, Sequence('task_id_seq'), primary_key=True)
    task_id = Column(String(1060),unique=True)
    name = Column(String(1024),unique=True)
    desc = Column(String(4096))
    project_name =  Column(String(1024))
    project_version = Column(String(50))
    create_time = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String(20))
    retcode = Column(Integer)
    #work_path = Column(String(4096))
    log_path = Column(String(4096))
    #uri = Column(String(4096))
    spider_config = Column(String(40960))

    @classmethod
    def from_task(cls,task):
        tm = cls()
        tm.task_id = task.task_id
        tm.name = task.name
        tm.desc = task.desc
        tm.project_name = task.project_name
        tm.project_version = task.project_version
        tm.create_time = task.create_time
        tm.start_time = task.start_time
        tm.end_time = task.end_time
        tm.status = task.status
        tm.retcode = task.retcode
        tm.log_path = task.log_path
        tm.spider_config = task.spider_config
        return tm



Base.metadata.create_all(db_engine)