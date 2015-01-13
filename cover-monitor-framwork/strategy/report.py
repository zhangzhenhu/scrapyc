from mako import template
from .strategy import Strategy
import operator 
import os 
import socket
class Report(Strategy):
    """docstring for Report"""
# -*- coding: utf-8 -*-

    def run(self,data):
        
        stats = self.fr.after_strategies_dict["statistic"]
        jobdir = self.settings["JOBDIR"]
        htf = self.settings["REPORT_HTML_TEMPLATE"]
        f=open(htf,"r")
        data=f.read().decode("gbk")
        f.close()
        casef = "wget ftp://%s%s"%(socket.gethostname(),os.path.join(jobdir,"result.xls"))
        t = template.Template(data, output_encoding="gbk")

        rf =os.path.join(jobdir,"report.html")
        f = open(rf,'w')
        f.write(t.render(STATS = stats,FTP=casef))
        f.close()
        
        email_bin = self.settings['REPORT_EMAIL_BIN']
        email_svr = self.settings['REPORT_EMAIL_SVR']
        email_title = self.settings['REPORT_EMAIL_TITLE']
        email_from = self.settings['REPORT_EMAIL_FROM']
        email_to = " -t ".join(self.settings['REPORT_EMAIL_TO'].split())
        log = os.path.join(jobdir,"email.log")
        err = os.path.join(jobdir,"email.err")

        cmd = "cat %s | %s  -s %s -u %s   -f %s -t %s  >%s  2>%s "%(rf,email_bin,email_svr,email_title,email_from,email_to,log,err)
        print "[Strategy:%s] cmd:%s"%(self.name,cmd )
        os.system(cmd)


