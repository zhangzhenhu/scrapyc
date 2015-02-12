# -*- coding: GBK -*-
import os

WORDIR=os.getcwd()
JOBDIR = os.path.join(WORDIR,"history","tmp")

BEFORE_STRATEGIES = [
"strategy.convert.Convert",
]

COMPONENTS = {
    #"component.pcccdb.PCCcdb" :None,
    "component.linkbase.Linkbase" :None,
    #"component.wiseccdb.WiseCcdb" :None,
    "component.l2linkbase.L2base" :None,
    "component.l2patch.L2Patch" :None,
    "component.ip.IP" :None,
    "component.forbid.Forbid" :None,
    "component.robots.Robots" :None,
    #"component.levelall.LevelAll" :None,
    # "component.dc" :None,
} 
AFTER_STRATEGIES = [
    "strategy.ccdb.CCDB",
    "strategy.common.Common",
    "strategy.robots.Robots",
    "strategy.linkbase.Linkbase",
    "strategy.forbid.Forbid",
    "strategy.ip.IP",
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
REPORT_EMAIL_TO ="zhangzhenhu@baidu.com baihongxia@baidu.com kangqiusheng@baidu.com wangchuangang@baidu.com zhangbo15@baidu.com wangxiaorong@baidu.com wangyuanqiong@baidu.com zhoutianhua@baidu.com litianhe@baidu.com wangyifang@baidu.com zhongxiande@baidu.com zhouguanglu01@baidu.com tianzhenlei@baidu.com wangtingting10@baidu.com"
REPORT_EMAIL_TO ="zhangzhenhu@baidu.com"
REPORT_EMAIL_SVR = "hotswap-in.baidu.com"
REPORT_EMAIL_TITLE = "国际化无线覆盖率监控"
REPORT_OWNER={
    "unCrawl":{"owner":"wangyifang@baidu.com","desc":u"""1. case站点流量手动上线

长线升级cc压力策略，保证中小站点流量 """},
    "notFound":{"owner":"zhangzhenhu@baidu.com","desc":u""" """},
    "noIP":{"owner":"liangdong01@baidu.com","desc":u""" """},
    "Forbidden":{"owner":"zhouguanglu01@baidu.com","desc":u"""1. 和站长谈判  预计3月初结论
2. 搭建日本出口 预计3月初完成
"""},
    "linkbaseDel":{"owner":"zhongxiande@baidu.com","desc":u"""短线配置白名单@钟贤德"""},
    "Forbidden_nm":{"owner":"zhouguanglu01@baidu.com","desc":u"""已配置匿名出口。需要持续关注效果@张博"""},
    "lowWeight":{"owner":"wangchuangang@baidu.com","desc":u""" """},
    "del_reason=61":{"owner":"zhongxiande@baidu.com","desc":u""" """},
    "del_reason=5":{"owner":"zhouguanglu01@baidu.com","desc":u"""play.google.com抓成中文被删除，可配置美国出口解决。@广露"""},
    "del_reason=24":{"owner":"xiongzhen@baidu.com","desc":u""" """},
    "del_reason=32":{"owner":"kangqiusheng@baidu.com","desc":u"""wise识别错误。
1.3月10号EC上线新版并进行刷库倒库
2.跟进识别招回效果@王婷婷"""},
    "del_reason=20":{"owner":"zhongxiande@baidu.com","desc":u"""短线配置白名单@钟贤德"""},
    "del_reason=1":{"owner":"","desc":u""" """},
    "del_reason=2":{"owner":"","desc":u""" """},
    "wiseEorr":{"owner":"wangtingting10@baidu.com","desc":u"""wise识别错误。
1.3月10号EC上线新版并进行刷库倒库
2.跟进识别招回效果@王婷婷
"""},
    "weight2":{"owner":"wangtingting10@baidu.com","desc":u"""wise识别错误。
1.3月10号EC上线新版并进行刷库倒库
2.跟进识别招回效果@王婷婷
"""},
    "weight10":{"owner":"wangtingting10@baidu.com","desc":u"""wise识别错误。
1.3月10号EC上线新版并进行刷库倒库
2.跟进识别招回效果@王婷婷
"""},

}

PC_SITE = ["www.facebook.com",
"www.imdb.com",
"www.stafaband.info",
"www.youtube.com",
"twitter.com",
"www.youtube.co.id",
"www.solopos.com",#自适配


]

PC_DOMAIN = [
".blogspot.com",
".wordpress.com",


]







CONVERT_REPLACE = {
    "http://www.facebook.com/profile.php?id=128290960576624":"http://www.facebook.com/pages/Info-Kerja-Keluar-Negeri/128290960576624",
    "http://www.facebook.com/profile.php?id=165369583498686":"http://www.facebook.com/pages/Johnny-Andrean-Salon/165369583498686",
"http://www.facebook.com/profile.php?id=189602504520875":"http://www.facebook.com/pages/Komunitas-Penggemar-Kereta-Api-Indonesia-PTKAI/189602504520875",
"http://www.facebook.com/profile.php?id=237498782997855":"http://www.facebook.com/pages/Rumah-Tante-Girang/237498782997855",
"http://www.facebook.com/profile.php?id=242270829269652":"http://www.facebook.com/pages/Asosiasi-Masinis-Indonesia/242270829269652",
"http://www.facebook.com/profile.php?id=359593697459316":"http://www.facebook.com/pages/REI-Adventure-Store-Malang/359593697459316",
"http://www.facebook.com/profile.php?id=443341195750480":"http://www.facebook.com/pages/Inna-Swinger/443341195750480",
"http://www.facebook.com/profile.php?id=498868210157756":"http://www.facebook.com/pages/Santhy-Agatha/498868210157756",
"http://www.facebook.com/profile.php?id=570283562995480":"http://www.facebook.com/pages/Baju-Murah-Harga-Mulai-40rb-Leira-Online-Shop-Grosir-eceran/570283562995480",
"http://www.facebook.com/profile.php?id=68304404153":"http://www.facebook.com/pages/Nam-Centre-Ballroom/68304404153",
    "http://www.facebook.com/profile.php?id=373368842775458":"http://www.facebook.com/pages/Artis-sexxx-SMP-SMA-gentoz-yukkkk/373368842775458",
    "http://www.facebook.com/profile.php?id=549782498377679":"http://www.facebook.com/pages/Cerita-sex-remaja-dan-dewasa/549782498377679"
}
