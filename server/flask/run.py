#!/home/spider/python/bin/python

# -*- coding: utf-8 -*-

from scrapyc.server.flask.app import flask_app,coreapp
from scrapyc.server.flask.views  import *

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

def execute():
    flask_app.config["coreapp"].start()
    flask_app.config["apscheduler"].start()

    #flask_app.run(debug=False)

    http_server = HTTPServer(WSGIContainer(flask_app))
    http_server.listen(5000)
    IOLoop.instance().start()

    flask_app.config["apscheduler"].shutdown(wait=True)
    flask_app.config["coreapp"].stop()

if __name__ == '__main__':
    execute()