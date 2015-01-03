from ..mako.template import Template
from .strategy import Strategy
import operator 
import os 

class Report(Strategy):
    """docstring for Report"""
# -*- coding: utf-8 -*-

    def run(self,data):
        
        stats = self.fr.strategies_dict["statistic"]
        template = self.settings["REPORT_HTML_TEMPLATE"]
        f=open(tmplate,"r")
        data=f.read().decode("gbk")
        t = Template(data, output_encoding="gbk")
        jobdir = self.settings["JOBDIR"]
        rf =os.path.join(jobdir,"report.html")
        f = open(rf,'w')
        f.write(t.render(STATS = stats))
        f.close()
        email_bin = self.settings['REPORT_EMAIL_BIN']
        email_svr = self.settings['REPORT_EMAIL_SVR']
        email_title = self.settings['REPORT_EMAIL_TITLE']
        email_from = self.settings['REPORT_EMAIL_FROM']
        email_to = " -t ".join(self.settings['REPORT_EMAIL_TO'].split())
        log = os.path.join(jobdir,"email.log")
        err = os.path.join(jobdir,"email.err")

        cmd = "cat %s | %s  -s %s -u %s   -f %s %s  >log  2>err "%(rf,email_bin,email_svr,email_title,email_from,email_to,log,err)
        os.system(cmd)

