



from scrapyc.server.flask.app import flask_app,coreapp
from scrapyc.server.flask.views  import *



flask_app.config["coreapp"].start()
flask_app.config["apscheduler"].start()
flask_app.run(debug=False)
flask_app.config["apscheduler"].shutdown(wait=True)
flask_app.config["coreapp"].stop()