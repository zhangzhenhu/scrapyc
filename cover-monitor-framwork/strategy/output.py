from .strategy import Strategy
import operator 
import os 

class Output(Strategy):
    """docstring for Output"""


    def run(self,data):
        print "[Strategy:Output] start"
        jobdir =self.settings["JOBDIR"]
        sf = os.path.join(jobdir,"result.xls")
        f = open(fs,"w")

        for case in data:
            f.write(case.origin.strip())
            for key in case._result_schema:
                if key in case.result:
                    value = case.result[key]
                else:
                    value = ""
                f.write("\t%s"%value)
            f.write("\n")

        f.close()
        print "[Strategy:Output] close"

            