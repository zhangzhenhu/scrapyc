# -*- coding: utf-8 -*-
"""


Authors: acmtiger@gmail.com
Date:    2015/11/16 9:42
"""

import os
import sys
import logging
from .settings import Settings


class CoreApp(object):
    """docstring for CoreApp"""
    config = Settings()
    scheduler = None

    def __init__(self):
        super(CoreApp, self).__init__()

    def init(self, setting_module=None):

        if setting_module == None:
            setting_module = os.environ["SCRAPYC_SETTINGS"]
        if setting_module:
            self.config.setmodule(setting_module)

        logging.basicConfig(format=self.config.get("LOG_FORMATER"), level=self.config.get("LOG_LEVEL", logging.INFO))

        for _path_config in ["LOG_PATH", "DATA_PATH", "PROJECT_PATH", "HISTORY_PATH"]:
            _p = self.config.get(_path_config)
            if not os.path.exists(_p):
                os.mkdir(_p)

        from core.scheduler import Scheduler
        self.scheduler = Scheduler(self.config)

    def start(self):
        self.scheduler.start()
        self.scheduler.project_reload()

    def stop(self):
        if self.scheduler:
            self.scheduler.stop()


coreapp = CoreApp()
