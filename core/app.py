# -*- coding: utf-8 -*-
"""


Authors: acmtiger@gmail.com
Date:    2015/11/16 9:42
"""

import os
import sys
import logging
from sqlalchemy import create_engine
from db.database import Base, SafeSession
from core.scheduler import Scheduler


class CoreApp(object):
    """
    """
    config = None
    scheduler = None

    def __init__(self, config):
        super(CoreApp, self).__init__()
        self.config = config

        self.__init_db()
        self.scheduler = Scheduler(self.config)

    def __init_db(self):

        _db_file = self.config.get("DATA_PATH", None)
        if _db_file:
            _db_file = os.path.join(_db_file, "task.db")
        else:
            _db_file = ':memory:'
        self.db_engine = create_engine('sqlite:///' + _db_file, echo=False)
        Base.metadata.create_all(self.db_engine)
        SafeSession.configure(bind=self.db_engine)

    def start(self):
        self.scheduler.start()
        self.scheduler.project_reload()

    def stop(self):
        if self.scheduler:
            self.scheduler.stop()


