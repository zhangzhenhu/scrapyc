#encoding=utf8
import os
import sys
import flask
from flaskext.xmlrpc import XMLRPCHandler,Fault
import logging

flask_app = flask.Flask( __name__ )
from scrapyc.server.core.app import coreapp

#os.environ["SCRAPYC_SETTINGS"] = "scrapyc.server.settings"
if os.path.exists("./settings.py") or os.path.exists("./settings.pyc"):
    coreapp.init("settings")
else:
    coreapp.init()

_log_file = os.path.join(coreapp.config.get("LOG_PATH"),"flask.log")
flask_app.logger.addHandler(logging.FileHandler(_log_file))

for _config in ["LOG_PATH","DATA_PATH","PROJECT_PATH","HISTORY_PATH"]:
    flask_app.config[_config] = coreapp.config[_config]


flask_app.config["coreapp"] = coreapp
flask_app.config["scheduler"] = coreapp.scheduler

#flask_app.config["db_session"] = coreapp.config.get("db_session")


from scrapyc.server.flask.proxy import SchedulerProxy
_handler = XMLRPCHandler('api')
_scheduler_proxy = SchedulerProxy(flask_app)
_handler.register_instance(_scheduler_proxy)
_handler.connect(flask_app, '/api')    
flask_app.config["scheduler_proxy"] = _scheduler_proxy


from apscheduler.schedulers.tornado import TornadoScheduler
import os

# The "apscheduler." prefix is hard coded
apscheduler = TornadoScheduler({
    'apscheduler.jobstores.default': {
        'type': 'sqlalchemy',
        'url': 'sqlite:///'+os.path.join(flask_app.config["DATA_PATH"],"apscheduler.db")
    },

    'apscheduler.job_defaults.coalesce': 'true',
    'apscheduler.job_defaults.max_instances': '1',
    #'apscheduler.timezone': 'CCT',
    
}) 

flask_app.config["apscheduler"] = apscheduler


