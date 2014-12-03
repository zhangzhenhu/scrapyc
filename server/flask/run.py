



from scrapyc.server.flask.app import flask_app,coreapp
from scrapyc.server.flask.views  import *

#from apscheduler.schedulers.background import BackgroundScheduler
import os

# The "apscheduler." prefix is hard coded
# apscheduler = BackgroundScheduler({
#     'apscheduler.jobstores.default': {
#         'type': 'sqlalchemy',
#         'url': 'sqlite:///'+os.path.join(flask_app.config["DATA_PATH"],"apscheduler.sqlite")
#     },
#     'apscheduler.executors.default': {
#         'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
#         'max_workers': '20'
#     },
#     'apscheduler.job_defaults.coalesce': 'false',
#     'apscheduler.job_defaults.max_instances': '1',
    
# })



flask_app.run(debug=False)

coreapp.clear()