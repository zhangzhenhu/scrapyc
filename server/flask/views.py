#encoding=utf8
# with app.open_resource('schema.sql') as f:
#     contents = f.read()
#     do_something_with(contents)
#     http://dormousehole.readthedocs.org/en/latest/api.html#application-object

from crawler import app
@app.route('/')
def index():
    return 'Hello World!'