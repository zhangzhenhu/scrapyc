


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
    def target(self):
        return self._target
    def set_target(self,target):
        self._target = target
        
    def set_data(name,value):
        self.data[name]=value
        