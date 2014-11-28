#encoding=utf8
import os
from importlib import import_module
from scrapyc.server.flask.app  import flask_app

#import settings
def main():


    #app = create_app("")   
    flask_app.debug = True
    flask_app.run()

if __name__ == '__main__':
    #default_setting_file = os.path.abspath( os.path.join(os.path.dirname(__file__)))
    #default_setting = import_module(default_setting_file)
    

    main()