# encoding=utf8
import os
import flask
import logging
from flaskext.xmlrpc import XMLRPCHandler, Fault
from config import load_config
from flask.ext.sqlalchemy import SQLAlchemy
from apscheduler.schedulers.tornado import TornadoScheduler
from core.app import coreapp
from webui.proxy import SchedulerProxy

flask_app = flask.Flask(__name__)
db = SQLAlchemy()


def init_app(flask_app):

    config = load_config()
    flask_app.config.from_object(config)
    ctx = flask_app.app_context()
    ctx.push()
    db.init_app(flask_app)
    db.create_all()

    _log_file = os.path.join(flask_app.config.get("LOG_PATH"), "flask.log")
    flask_app.logger.addHandler(logging.FileHandler(_log_file))
    #
    flask_app.config["coreapp"] = coreapp
    flask_app.config["scheduler"] = coreapp.scheduler

# flask_app.config["db_session"] = coreapp.config.get("db_session")

    _handler = XMLRPCHandler('api')
    _scheduler_proxy = SchedulerProxy(flask_app)
    _handler.register_instance(_scheduler_proxy)
    _handler.connect(flask_app, '/api')
    flask_app.config["scheduler_proxy"] = _scheduler_proxy

    # The "apscheduler." prefix is hard coded

    apscheduler = TornadoScheduler({
        'apscheduler.jobstores.default': {
            'type': 'sqlalchemy',
            'url': 'sqlite:///' + os.path.join(flask_app.config["DATA_PATH"], "apscheduler.db")
        },

        'apscheduler.job_defaults.coalesce': 'true',
        'apscheduler.job_defaults.max_instances': '1',
        # 'apscheduler.timezone': 'CCT',

    })

    flask_app.config["apscheduler"] = apscheduler
