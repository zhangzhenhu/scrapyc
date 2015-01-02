from .strategy import Strategy
import operator 
import os 

class Statistic(Strategy):
    """docstring for Statistic"""
# -*- coding: utf-8 -*-

    def run(self,data):
        
        stats = {}

        for case in data:
            res = case.result
            if res["conclusion"] not in stats:
                stats[res["conclusion"]] = 1
            else:
                stats[res["conclusion"]] += 1

        jobdir =self.settings["JOBDIR"]
        sf = os.path.join(jobdir,"stats.txt")
        f = open(sf,"w")
        total = len(data)
        for key,value in sorted(stats.iteritems(), key=operator.itemgetter(1), reverse=True)  :
            f.write("%s\t%d\t%.3f\n"%(key,value,value/float(total)))
        f.write("Toal\t%d\t1.000\n"%(total,))
        f.close()

            