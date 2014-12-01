#encoding=utf8
# with app.open_resource('schema.sql') as f:
#     contents = f.read()
#     do_something_with(contents)
#     http://dormousehole.readthedocs.org/en/latest/api.html#application-object

from scrapyc.server.flask.app import flask_app
from flask import render_template


@flask_app.route('/')
def index():
    return render_template('index.html', flask_app=flask_app)