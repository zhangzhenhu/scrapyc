"""
This module contains the default values for all settings used by Scrapy.

For more information about these settings you can read the settings
documentation in docs/topics/settings.rst

Scrapy developers, if you add a setting here remember to:

* add it in alphabetical order
* group similar settings without leaving blank lines
* add its documentation to the available settings documentation
  (docs/topics/settings.rst)

"""

import os
import sys
from importlib import import_module
from os.path import join, abspath, dirname
import logging

WORK_PATH=os.getcwd()
LOG_PATH = os.path.join(WORK_PATH,"log")
DATA_PATH = os.path.join(WORK_PATH,"data")
PROJECT_PATH = os.path.join(WORK_PATH,"projects")
HISTORY_PATH = os.path.join(WORK_PATH,"history")
LOG_LEVEL = logging.DEBUG
LOG_FORMATER = "%(asctime)s [%(filename)s::%(funcName)s:%(lineno)d] %(levelname)s %(message)s"
MAX_RUN_TASK = 10