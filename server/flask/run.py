



from scrapyc.server.flask.app import flask_app,coreapp
from scrapyc.server.flask.views  import *

flask_app.run(debug=False)
coreapp.clear()