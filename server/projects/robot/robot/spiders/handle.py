#encoding=UTF8
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc

from scrapy import signals
from robot.items import NimeiItem
from robot.spiders import base
import scrapy
from scrapyc.server.utils.url import get_url_site,get_url_scheme
import urlparse
import re
import datetime
import string

class HandleSpider(base.RobotSpider):
    name = "handle"

    allowed_domains = []
    start_urls = [    ]
    def start_requests(self):

        yield scrapy.Request("http://nccur.lib.nccu.edu.tw/browse-title",callback=self.parse)
        yield scrapy.Request("http://thesis.lib.ncu.edu.tw/browse-title",callback=self.parse)
        yield scrapy.Request("http://ir.lib.ncu.edu.tw/browse-title",callback=self.parse)
        yield scrapy.Request("http://nchuir.lib.nchu.edu.tw/browse-title",callback=self.parse)
        yield scrapy.Request("http://hermes-ir.lib.hit-u.ac.jp/rs/browse-title",callback=self.parse)
        # yield scrapy.Request("")
        for item in super(HandleSpider, self).start_requests():
            yield item        


    def parse(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return
        base_url  = get_base_url(response)
        for href in response.xpath('//table/tr/td/strong/a/@href').extract():
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
            #self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)
            #yield scrapy.Request(url=abs_url,callback=self.parse)

        #解析pdf
        for href in response.xpath('//table[@class="object_table"]/tr/td[4]/a/@href').extract():
            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
            #self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)
            #yield scrapy.Request(url=abs_url,callback=self.parse)

        #解析翻页
        for href in response.xpath('//table/tr/td/table/tr/td/a/@href').extract():
            if ("page=" not in href  and "browse-title?top=" not in href ) or "itemsPerPage=" in href:
                continue

            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
            #self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)
            yield scrapy.Request(url=abs_url,callback=self.parse)


class HandleCNSpider(base.RobotSpider):
    name = "handle_cn"

    allowed_domains = []
    start_urls = [    ]
    def start_requests(self):
        #人工的
        yield scrapy.Request("http://www.irgrid.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.las.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://dspace.imech.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.sia.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.ioe.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://210.75.237.14/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://210.77.90.120/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://222.77.69.102:8089/qzyx/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://icsnn2010.semi.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.nsl.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://159.226.240.226/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://210.39.5.17/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://210.77.64.217/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.psych.ac.cn:8080/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://124.16.151.184/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://202.127.25.144/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.cumt.edu.cn:8080/browse?type=title",callback=self.parse_first)
        #筛选的
        yield scrapy.Request("http://www.alice.cnptia.embrapa.br/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://www.infoteca.cnptia.embrapa.br/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.casipm.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.ceode.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.ciomp.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.csdl.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://cas-ir.dicp.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://www.cas-ir.dicp.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.etp.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.fjirsm.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.gibh.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.giec.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.gig.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.hfcas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.ibcas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.iccas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.iga.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.igsnrr.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.ihb.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.ihep.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://catalogs.ihns.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.ihns.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.imde.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://dspace.imech.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://impcas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ads-anmke.impcas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ads-ke.impcas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ads-linacke.impcas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ads-ndke.impcas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ads-stke.impcas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ads-tcke.impcas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.impcas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://library.impcas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://asmt.imr.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://fhtc.imr.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.imr.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.ioa.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.ioe.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.ipe.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.iphy.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ircnic.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://www.ircnic.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://www.irgrid.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.iscas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.isl.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.iswc.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.itp.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.itpcas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.kib.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.las.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://lbwyy.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://www.lbwyy.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.licp.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.lig.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://service.llas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.neigae.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.niaot.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://niglaslib.niglas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.nigpas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.nimte.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.nsl.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.nssc.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.nwipb.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.opt.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://dse.pmo.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ephemerial.pmo.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://hea.pmo.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://libir.pmo.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.psych.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.qdio.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.qibebt.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.radi.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.rcees.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://library.rcees.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.sari.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.scbg.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.scsio.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://icsnn2010.semi.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.semi.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.shao.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.sibs.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.sic.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.simm.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.sinano.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.sinap.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://sinapir.sinap.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.sioc.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.ucas.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.whigg.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.wipm.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.xao.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.yic.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.ynao.ac.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.xjipc.cas.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://oa.sloc.com.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://byir.bupt.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.fjzs.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://lib.gdcc.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.gdufs.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.gxun.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://lib5.hkc.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://lib6.hkc.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.lzu.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.mnnu.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.pku.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.shzu.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://oaps.lib.sjtu.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.synu.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.lib.szu.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.lib.tsinghua.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://oaps.lib.tsinghua.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.ustb.edu.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://dspace.xmu.edu.cn/dspace/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.ieecas.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.iet.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.ciac.jl.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.xtbg.org.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://www.realax.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.sia.cn/browse?type=dateissued",callback=self.parse_first)
        yield scrapy.Request("http://ir.stlib.cn/browse?type=dateissued",callback=self.parse_first)

        # yield scrapy.Request("")
        for item in super(HandleCNSpider, self).start_requests():
            yield item        


    def parse_first(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return 
        ret = re.search("var totalItemCount = (\d+);",response.body)
        totalItemCount = 0
        if ret:
            totalItemCount = int(ret.groups()[0])
            self.log("Parse %s totalItemCount %d"%(response.url,totalItemCount),level=scrapy.log.INFO)
        else:
            self.log("Parse %s totalItemCount NULL"%(response.url),level=scrapy.log.INFO)
        offset = 0
        #site = get_url_site(response.url)
        while offset < totalItemCount:
            yield scrapy.Request(response.url.replace("browse?type=dateissued","browse?order=DESC&rpp=100&sort_by=2&year=&offset=%d&type=dateissued"%(offset)),callback=self.parse)
            offset += 100

    def parse(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            return 
        base_url  = get_base_url(response)
        for href in response.xpath('//form[@name="itemlist"]/table/tr[@class="itemLine"]/td/span/a/@href').extract():
            relative_url = href
            if relative_url.startswith("/simple-search?"):
                continue

            abs_url =urljoin_rfc(base_url,relative_url.split("?",1)[0])
            yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
            #self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)
            #yield scrapy.Request(url=abs_url,callback=self.parse)


