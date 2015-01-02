from .strategy import Strategy
import operator 
import os 

class Close(Strategy):
    """docstring for Close"""


    def run(self,data):
        

        for case in data:
            case.set_result("conclusion","Unkown")
            case.close = True

            