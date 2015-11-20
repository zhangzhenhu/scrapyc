# -*- coding: cp936 -*-
from datetime import datetime

from twisted.web import resource, static
from twisted.application.service import IServiceCollection

from scrapy.utils.misc import load_object

from .interfaces import IPoller, IEggStorage, ISpiderScheduler
import os
import scrapyd
class Root(resource.Resource):

    def __init__(self, config, app):
        resource.Resource.__init__(self)
        self.config=config
        self.debug = config.getboolean('debug', False)
        self.runner = config.get('runner')
        logsdir = config.get('logs_dir')
        itemsdir = config.get('items_dir')
        self.app = app
        self.static_path=os.path.join(scrapyd.__path__[0],'static')
        self.putChild('', Home(self))
        if logsdir:
            self.putChild('logs', static.File(logsdir, 'text/plain'))
        if itemsdir:
            self.putChild('items', static.File(itemsdir, 'text/plain'))
        self.putChild('jobs', Jobs(self))
        
        self.putChild('static',static.File(os.path.join(scrapyd.__path__[0],'static'), 'text/plain'))
        services = config.items('services', ())
        for servName, servClsName in services:
          servCls = load_object(servClsName)
          self.putChild(servName, servCls(self))
        self.update_projects()

    def update_projects(self):
        self.poller.update_projects()
        self.scheduler.update_projects()

    @property
    def launcher(self):
        app = IServiceCollection(self.app, self.app)
        return app.getServiceNamed('launcher')

    @property
    def scheduler(self):
        return self.app.getComponent(ISpiderScheduler)

    @property
    def eggstorage(self):
        return self.app.getComponent(IEggStorage)

    @property
    def poller(self):
        return self.app.getComponent(IPoller)


class Home(resource.Resource):

    def __init__(self, root):
        resource.Resource.__init__(self)
        self.root = root
        self.home_page=os.path.join(self.root.static_path,'home.html')

    def render_GET(self, txrequest):
        vars = {
            'projects': ', '.join(self.root.scheduler.list_projects()),
        }
        f=open(self.home_page,"r")
        html=f.read()
        f.close()
        return html
        
        return """
<html>
<head><title>Scrapyd</title></head>
<body>
<h1>Scrapyd</h1>
<p>Available projects: <b>%(projects)s</b></p>
<ul>
<li><a href="/jobs">Jobs</a></li>
<li><a href="/items/">Items</li>
<li><a href="/logs/">Logs</li>
<li><a href="http://doc.scrapy.org/en/latest/topics/scrapyd.html">Documentation</a></li>
</ul>

<h2>How to schedule a spider?</h2>

<p>To schedule a spider you need to use the API (this web UI is only for
monitoring)</p>

<p>Example using <a href="http://curl.haxx.se/">curl</a>:</p>
<p><code>curl http://localhost:6800/schedule.json -d project=default -d spider=somespider</code></p>

<p>For more information about the API, see the <a href="http://doc.scrapy.org/en/latest/topics/scrapyd.html">Scrapyd documentation</a></p>
</body>
</html>
""" % vars


class Jobs(resource.Resource):

    def __init__(self, root):
        resource.Resource.__init__(self)
        self.root = root

    def render(self, txrequest):
        s = ""
       
        s += "<h1>Jobs</h1>"
       
        s += "<table border='1'>"
        s += "<th>Project</th><th>Spider</th><th>Job</th><th>PID</th><th>start_time</th><th>Runtime</th><th>end_time</th><th>Log</th><th>Items</th><th>action</th>"
        s += "<tr><th colspan='10' style='background-color: #ddd'>Pending</th></tr>"
        for project, queue in self.root.poller.queues.items():
            for m in queue.list():
                s += "<tr>"
                s += "<td>%s</td>" % project
                s += "<td>%s</td>" % str(m['name'])
                s += "<td>%s</td>" % str(m['_job'])
                s += "</tr>"
        s += "<tr><th colspan='10' style='background-color: #ddd'>Running</th></tr>"
        for p in self.root.launcher.processes.values():
            s += "<tr>"
            for a in ['project', 'spider', 'job', 'pid','start_time']:
                s += "<td>%s</td>" % getattr(p, a)
            s += "<td>%s</td>" % (datetime.now() - p.start_time)
            s += "<td></td>"
            s += "<td><a href='/logs/%s/%s/%s.log'>Log</a></td>" % (p.project, p.spider, p.job)
            s += "<td><a href='/items/%s/%s/%s.jl'>Items</a></td>" % (p.project, p.spider, p.job)
            s += "<td><a href='javascript:void(0);' onclick='kill_job(\"%s\");'>kill</a></td>" % p.job
            s += "</tr>"
        s += "<tr><th colspan='10' style='background-color: #ddd'>Finished</th></tr>"
        for p in sorted(self.root.launcher.finished,key=lambda d:d.start_time ):
            s += "<tr>"
            for a in ['project', 'spider', 'job']:
                s += "<td>%s</td>" % getattr(p, a)
                
            s += "<td></td>"
            s += "<td>%s</td>" % p.start_time
            s += "<td>%s</td>" % (p.end_time - p.start_time)
            s += "<td>%s</td>" % p.end_time
            s += "<td><a href='/logs/%s/%s/%s.log'>Log</a></td>" % (p.project, p.spider, p.job)
            s += "<td><a href='/items/%s/%s/%s.jl'>Items</a></td>" % (p.project, p.spider, p.job)
            s += "<td></td>"
            s += "</tr>"
        s += "</table>"
        s += "</body>"
        s += "</html>"
        return s
