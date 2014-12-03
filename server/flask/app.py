#encoding=utf8
import os
import sys
import flask
from flaskext.xmlrpc import XMLRPCHandler,Fault
import logging

os.environ["SCRAPYC_SETTINGS"] = "scrapyc.server.settings"
flask_app = flask.Flask( __name__ )


#project_settings = os.environ("SCRAPYC_SETTINGS")
from scrapyc.server.core.app import coreapp
coreapp.init()

flask_app.config.from_envvar('SCRAPYC_SETTINGS',silent=True)

_log_file = os.path.join(coreapp.config.get("LOG_PATH"),"flask.log")
flask_app.logger.addHandler(logging.FileHandler(_log_file))

for _config in ["LOG_PATH","DATA_PATH","PROJECT_PATH","HISTORY_PATH"]:
    flask_app.config[_config] = coreapp.config[_config]
flask_app.config["scheduler"] = coreapp.scheduler

#flask_app.config["db_session"] = coreapp.config.get("db_session")


from scrapyc.server.flask.proxy import SchedulerProxy
_handler = XMLRPCHandler('api')
_scheduler_proxy = SchedulerProxy(flask_app)
_handler.register_instance(_scheduler_proxy)
_handler.connect(flask_app, '/api')    
flask_app.config["scheduler_proxy"] = _scheduler_proxy


    




