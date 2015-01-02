# -*- coding: utf-8 -*-


class Strategy(object):
    """docstring for Strategy"""
    def __init__(self, arg,fr):
        super(Strategy, self).__init__()
        self.settings = arg
        self.fr = fr


    def run(self,data):
        pass
        