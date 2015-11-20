# -*- coding: utf-8 -*-
"""
入口

Authors: acmtiger@gmail.com
Date:    2015/11/16 9:42
"""
import os
from webui.app import flask_app
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import logging
from flaskext.xmlrpc import XMLRPCHandler, Fault
from config import load_config
from apscheduler.schedulers.tornado import TornadoScheduler
from core.app import CoreApp
from webui.proxy import SchedulerProxy


def init_flask_app(config):



    ctx = flask_app.app_context()
    ctx.push()

    _log_file = os.path.join(flask_app.config.get("LOG_PATH"), "flask.log")
    flask_app.logger.addHandler(logging.FileHandler(_log_file))
    from webui.views import *
    return flask_app


def init_core_app(config):
    #
    coreapp = CoreApp(config)
    flask_app.config["coreapp"] = coreapp
    flask_app.config["scheduler"] = coreapp.scheduler

# flask_app.config["db_session"] = coreapp.config.get("db_session")

    _handler = XMLRPCHandler('api')
    _scheduler_proxy = SchedulerProxy(flask_app)
    _handler.register_instance(_scheduler_proxy)
    _handler.connect(flask_app, '/api')
    flask_app.config["scheduler_proxy"] = _scheduler_proxy

    # The "apscheduler." prefix is hard coded
    return coreapp


def init_apsscheduler(config):

    apscheduler = TornadoScheduler({
        'apscheduler.jobstores.default': {
            'type': 'sqlalchemy',
            'url': 'sqlite:///' + os.path.join(config["DATA_PATH"], "apscheduler.db")
        },

        'apscheduler.job_defaults.coalesce': 'true',
        'apscheduler.job_defaults.max_instances': '1',
        # 'apscheduler.timezone': 'CCT',

    })

    flask_app.config["apscheduler"] = apscheduler
    return apscheduler


def init_config(config):

    logging.basicConfig(format=config.get('LOG_FORMATER'), level=config.get("LOG_LEVEL", logging.INFO))
    for _path_config in ["LOG_PATH", "DATA_PATH", "PROJECT_PATH", "HISTORY_PATH"]:
        _p = config.get(_path_config)
        if not os.path.exists(_p):
            os.mkdir(_p)


def execute(config):


    core_app = init_core_app(config)
    init_flask_app(config)
    apscheduler = init_apsscheduler(config)

    core_app.start()
    apscheduler.start()

    # flask_app.run(debug=False)

    http_server = HTTPServer(WSGIContainer(flask_app))
    http_server.listen(8080, "0.0.0.0")
    IOLoop.instance().start()

    apscheduler.shutdown(wait=True)
    core_app.stop()


if __name__ == '__main__':

    config = load_config('LOCAL')
    flask_app.config.from_object(config)
    config = flask_app.config
    config["HOME_PATH"] = os.path.split(os.path.realpath(__file__))[0]
    init_config(config)

    execute(config)
