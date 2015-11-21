# -*- coding: utf-8 -*-
"""
对外提供的rpc接口

Authors: acmtiger@gmail.com
Date:    2015/11/16 9:42
"""


class SchedulerProxy(object):
    """docstring for SchedulerProxy"""

    def __init__(self, app):
        super(SchedulerProxy, self).__init__()
        self.app = app
        self._scheduler = app.config["scheduler"]

    def task_start(self, *args, **kwargs):

        return self._scheduler.task_start(*args, **kwargs)

    def task_kill(self, task_id):
        return self._scheduler.task_kill(task_id)

    def task_stop(self, task_id):
        return self._scheduler.task_stop(task_id)

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

    def history_page(self, pagenum, pagecount=10):
        r = []
        items, cur, total_page, page_count, total_count = self._scheduler.history_queue.page(pagenum, pagecount)
        for c in items:
            r.append(c.to_dict())
        return r, cur, total_page, page_count, total_count

    def history_count(self):
        return self._scheduler.history_queue.count()
        pass

    def history_by_taskid(self, task_id):
        pass

    def history_by_project(self, project_name, limit=None):
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
