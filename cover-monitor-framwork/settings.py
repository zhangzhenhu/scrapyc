# -*- coding: GBK -*-
import os

WORDIR=os.getcwd()
JOBDIR = os.path.join(WORDIR,"history")


COMPONENTS = {
    "component.pcccdb.PCCcdb" :None,
    "component.linkbase.Linkbase" :None,
    "component.wiseccdb.WiseCcdb" :None,
    "component.l2linkbase.L2base" :None,
    "component.l2patch.L2Patch" :None,
    # "component.robots" :None,
    # "component.dc" :None,
} 
STRATEGIES = [
    "strategy.ccdb.CCDB",
    "strategy.linkbase.Linkbase",
    "strategy.close.Close",
    "strategy.output.Output",
    "strategy.statistic.Statistic",
    # "strategy.weight":None,
    # "strategy.valid":None,
    
]

REPORT_HTML_TEMPLATE="./strategy/template.html"
REPORT_EMAIL_BIN = "/home/spider/share/common/sendEmail"
import socket
REPORT_EMAIL_FROM = socket.gethostname()
REPORT_EMAIL_TO ="zhangzhenhu"
REPORT_EMAIL_SVR = "hotswap-in.baidu.com"
REPORT_EMAIL_TITLE = "国际化无线覆盖率监控"