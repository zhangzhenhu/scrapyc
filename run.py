# -*- coding: utf-8 -*-
"""
入口

Authors: acmtiger@gmail.com
Date:    2015/11/16 9:42
"""
from webui.app import flask_app, init_app
from webui.views import *
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


def execute():
    flask_app.config["coreapp"].start()
    flask_app.config["apscheduler"].start()

    # flask_app.run(debug=False)

    http_server = HTTPServer(WSGIContainer(flask_app))
    http_server.listen(8080, "0.0.0.0")
    IOLoop.instance().start()

    flask_app.config["apscheduler"].shutdown(wait=True)
    flask_app.config["coreapp"].stop()


if __name__ == '__main__':

    init_app(flask_app)
    execute()
