from .strategy import Strategy
import operator 
import os 

class Statistic(Strategy):
    """docstring for Statistic"""
# -*- coding: utf-8 -*-
    name = "statistic"

    def run(self,data):
        
       
        self.count_total = 0
        self.count_valid = 0
        self.count_invalid = 0
        self.count_ok = 0
        self.stats_invalid = {}
        self.stats_valid = {}
        self.stats_ok = {}
        for case in data:
            res = case.result
            self.count_total +=1
            if case.ok :
                stats =  self.stats_ok
                self.count_ok +=1                
            elif case.valid :
                stats =  self.stats_valid
                self.count_valid +=1
            else:
                self.count_invalid +=1
                stats =  self.stats_invalid = {}

            if res["conclusion"] not in stats:
                stats[res["conclusion"]] = 1
            else:
                stats[res["conclusion"]] += 1
            
        #self.fr.set_data("stats",stats)
        jobdir =self.settings["JOBDIR"]
        sf = os.path.join(jobdir,"stats.txt")
        f = open(sf,"w")
        #total = len(data)
        for key,value in sorted(self.stats_ok.iteritems(), key=operator.itemgetter(1), reverse=True)  :
            f.write("%s\t%d\t%.3f\n"%(key,value,value/float(self.count_valid+self.count_ok)))

        for key,value in sorted(self.stats_valid.iteritems(), key=operator.itemgetter(1), reverse=True)  :
            f.write("%s\t%d\t%.3f\n"%(key,value,value/float(self.count_valid+self.count_ok)))
        for key,value in sorted(self.stats_invalid.iteritems(), key=operator.itemgetter(1), reverse=True)  :
            f.write("%s\t%d\tnull\n"%(key,value))


        f.write("Ok\t%d\t%.3f\n"%(self.count_ok,self.count_ok/float(self.count_valid+self.count_ok)))
        f.write("Case\t%d\t%.3f\n"%(self.count_valid,self.count_valid/float(self.count_valid+self.count_ok)))
        f.write("Valid\t%d\tnull\n"%(self.count_valid+self.count_ok))
        f.write("Toal\t%d\tnull\n"%(self.count_total,))
        f.close()


            