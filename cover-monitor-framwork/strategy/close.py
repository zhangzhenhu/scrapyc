from .strategy import Strategy
import operator 
import os 

class Close(Strategy):
    """docstring for Close"""


    def run(self,data):
        

        for case in data:
            if case.close :
                continue
            case.set_result("conclusion","Unkown")
            case.close = True

            