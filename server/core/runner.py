import sys
import os
import shutil
import tempfile
from contextlib import contextmanager


@contextmanager
def project_environment():
    #project = os.environ['SCRAPY_PROJECT_PATH']
    #os.chdir(project)
    #sys.path.append(project)
    print "[cwd]"
    print os.getcwd() 
    print "[sys.path]"
    for path in sys.path:
       print path 
    print "[cmdline]"
    print sys.argv
    sys.stderr.flush()
    sys.stdout.flush()
    

   
    
    yield
    return

def main():
    
   

    with project_environment():
        from scrapy.cmdline import execute
        execute()

if __name__ == '__main__':
   
    #os.environ['SCRAPY_PROJECT_PATH'] = "C:\Python27\Lib\site-packages\scrapyc\server\projects\csdn"
    #os.environ['SCRAPY_LOG_FILE'] = "C:\Python27\Lib\site-packages\scrapyc\server\history\test\csdn.log"
    #os.environ.setdefault('SCRAPY_SETTINGS_MODULE', "csdn.settings")
    main()
