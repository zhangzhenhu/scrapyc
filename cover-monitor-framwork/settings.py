# -*- coding: GBK -*-
import os

WORDIR=os.getcwd()
JOBDIR = os.path.join(WORDIR,"history","tmp")

BEFORE_STRATEGIES = [
"strategy.convert.Convert",
]

COMPONENTS = {
    "component.pcccdb.PCCcdb" :None,
    "component.linkbase.Linkbase" :None,
    "component.wiseccdb.WiseCcdb" :None,
    "component.l2linkbase.L2base" :None,
    "component.l2patch.L2Patch" :None,
    #"component.levelselect.LevelSelect" :None,
    #"component.levelall.LevelAll" :None,
    # "component.dc" :None,
} 
AFTER_STRATEGIES = [
    "strategy.ccdb.CCDB",
    "strategy.common.Common",
    "strategy.linkbase.Linkbase",
    "strategy.select.Select",
    "strategy.close.Close",
    "strategy.output.Output",
    "strategy.statistic.Statistic",
    "strategy.report.Report",
    # "strategy.weight":None,
    # "strategy.valid":None,
    
]

REPORT_HTML_TEMPLATE="./strategy/template.html"
REPORT_EMAIL_BIN = "/home/spider/share/common/sendEmail"
import socket
REPORT_EMAIL_FROM = socket.gethostname()
REPORT_EMAIL_TO ="zhangzhenhu@baidu.com baihongxia@baidu.com kangqiusheng@baidu.com wangchuangang@baidu.com zhangbo15@baidu.com wangxiaorong@baidu.com wangyuanqiong@baidu.com zhoutianhua@baidu.com"
#REPORT_EMAIL_TO ="zhangzhenhu@baidu.com"
REPORT_EMAIL_SVR = "hotswap-in.baidu.com"
REPORT_EMAIL_TITLE = "国际化无线覆盖率监控"
