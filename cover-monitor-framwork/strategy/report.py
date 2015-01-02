from ..mako.template import Template
from .strategy import Strategy
import operator 
import os 

class Report(Strategy):
    """docstring for Report"""
# -*- coding: utf-8 -*-

    def run(self,data):
        
        stats = self.fr.get_data("stats")
        


