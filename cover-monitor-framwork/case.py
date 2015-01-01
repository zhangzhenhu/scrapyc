import threading


class Case(object):
    """docstring for Case"""
    def __init__(self, arg,line):
        super(Case, self).__init__()
        self.settings = arg
        self.origin = line
        line=line.strip().split("\t")
        self.objurl = line[0]
        self.other=line[1:]
        self._target = self.objurl
        self.data = {}
        self._lock = threading.RLock()
        self._close = False
        self._result = {

        }
        self._result_schema = [       
        "conclusion",
        "reason",
        "basis",
        "additional",
        "solution",
        "owner",
        ]


    @property
    def target(self):
        return self._target
    @target.setter
    def target(self, value):
        self._target = value
    
    def get_data(self,name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def set_data(self,name,value):
        if self._lock.acquire():
            self.data[name]=value
        self._lock.release()

    def set_result(self,name,value):
        if name in self._result_schema:
            self._result[name]=value
            return True
        return False
        
    @property
    def close(self):
        return self._close
    @close.setter
    def close(self, value):
        self._close = value


    def __str__(self):
        s = self.objurl + "\t".join(self.other)
        for key in self._result_schema:
            if key in self._result:
                v = self._result[key]
            else:
                v = ""
            s += "\t" + v
        return s


        