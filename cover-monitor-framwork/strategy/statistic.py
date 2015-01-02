from .strategy import Strategy
import operator 
import os 

class Statistic(Strategy):
    """docstring for Statistic"""
# -*- coding: utf-8 -*-

    def run(self,data):
        
        stats = {"_valid_":0,"_total_":0}

        for case in data:
            res = case.result
            if res["conclusion"] not in stats:
                stats[res["conclusion"]] = 1
            else:
                stats[res["conclusion"]] += 1
            if case.valid :
                stats["_valid_"] += 1
            stats["_total_"] += 1

        self.fr.set_data("stats",stats)
        jobdir =self.settings["JOBDIR"]
        sf = os.path.join(jobdir,"stats.txt")
        f = open(sf,"w")
        #total = len(data)
        for key,value in sorted(stats.iteritems(), key=operator.itemgetter(1), reverse=True)  :
            f.write("%s\t%d\t%.3f\n"%(key,value,value/float(stats["_valid_"])))
        #f.write("Toal\t%d\t1.000\n"%(total,))
        f.close()


            