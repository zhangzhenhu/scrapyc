

class SchedulerProxy(object):
    """docstring for SchedulerProxy"""
    def __init__(self, app):
        super(SchedulerProxy, self).__init__()
        self.app = app
        self._scheduler = app.config["scheduler"]

    def task_start(self,project_name,spider_name,task_name,spider_params):

        return self._scheduler.task_start(project_name,spider_name,task_name,spider_params)

    def task_kill(self,task_id):
        pass

    def task_all(self):
        r = []
        for t in self._scheduler.task_all():
            
            r.append(t.to_dict())
        return r
    def task_count(self):
        
        return self._scheduler.task_count()


    def history_all(self):
        r = []
        for c in self._scheduler.history_all():
            r.append(c.to_dict())
        return r

    def history_by_taskid(self,task_id):
        pass

    def history_by_project(self,project_name,limit=None):
        pass
    

    def project_count(self):
        return self._scheduler.project_count()

    def project_all(self):
        r = []
        for c in self._scheduler.project_all():
            r.append(c.to_dict())
        return r


    def project_reload(self):
        return self._scheduler.project_reload()

    def project_get(self):
        pass


