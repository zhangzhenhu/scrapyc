# -*- coding: utf-8 -*-


class Strategy(object):
    """docstring for Strategy"""
    name = "strategy"
    def __init__(self, arg,fr):
        super(Strategy, self).__init__()
        self.settings = arg
        self.fr = fr
        if not self.name:
            self.name = self.__class__.lower()


    def run(self,data):
        pass
        