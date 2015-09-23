#encoding=UTF8
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc,url_query_cleaner

from scrapy import signals
from robot.items import NimeiItem
from robot.spiders import base
import scrapy
from scrapyc.server.utils.url import get_url_site,get_url_scheme
import urlparse
import re
import datetime
import string

class RobotSpider(base.RobotSpider):
    name = "tiller"

    allowed_domains = []
    start_urls = [    ]
    def start_requests(self):

        yield scrapy.Request("http://hdxbzkb.cnjournals.net/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.marinejournal.cn/hyyhz/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.cjmit.com/cjmit/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.hjkx.ac.cn/hjkx/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://211.68.236.122/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://hjjcgl.cnjournals.net/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://hnxbw.cnjournals.net/hznydxsk/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://journal.bit.edu.cn/sk/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://journals.hut.edu.cn/bz/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://journals.hut.edu.cn/sk/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://jsuese.scu.edu.cn/jsuese_cn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://jzclxb.allmaga.net/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://lfyff.zzu.edu.cn/lfyff/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://myfj.cnjournals.com/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://nhqks.cnjournals.com/yx/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://pedologica.issas.ac.cn/trxb/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://press.dlut.edu.cn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://rmme.ijournal.cn/rmme/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://science.ijournals.cn/jsunature_cn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://tyky.cnjournals.cn/tykycn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.actasc.cn/hjkxxb/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.aes.org.cn/nyhjkxxb/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.ajsmmu.cn/ajsmmu/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.biother.org/zgzlswzlzz/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.bxyjg.com/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.chinaminingmagazine.com/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.cjee.ac.cn/teepc_cn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.cjig.cn/jig/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.cjmit.com/cjiit/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.cjmit.com/cjmit/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.cjrmp.net/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.c-s-a.org.cn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.csis.cn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.cspine.org.cn/zgjzjszz/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.dqkxqk.ac.cn/dqkx/dqkx/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.ejotm.com/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.fxcsxb.com/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.hjkx.ac.cn/hjkx/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.hyxb.org.cn/aos/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.inforhubei.com/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.j-csam.org/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.jlis.cn/jtlsc/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.jmcchina.org/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.joelcn.com/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.jos.ac.cn/bdtxbcn/ch/reader/issue_browser_new.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.jsjkx.com/jsjkx/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.knittingpub.com/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.lsyslgy.com/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.lykxyj.com/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.lyxuebao.net/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.modernradar.cn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.plantprotection.ac.cn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.rehabi.com.cn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.semiopto.net/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.shhydxxb.com/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.smylz.cn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.spinejournal.net/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.syfjxzz.com/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.teleonline.cn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.tiprpress.com/xdywlc/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.tjzhongyiyao.com/tjzyy/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.tribology.com.cn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.wjhxxb.cn/wjhxxbcn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.xnxbz.net/xbnlkjdxzr/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.zgys.org/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://www.zwbhxb.cn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://xuebao.ahtcm.edu.cn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://ythx.scu.edu.cn/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://zgbjyx.alljournal.net.cn/zgbjyxzz/ch/reader/issue_browser.aspx",callback=self.parse_index)
        yield scrapy.Request("http://zjyxzzs.com/ch/reader/issue_browser.aspx",callback=self.parse_index)

        for item in super(RobotSpider, self).start_requests():
            yield item        
    #PATTERN1=re.compile(".*thread\-\d+\-\d+\-\d+\.html.*")

    def parse(self,response):

        if "issue_browser.aspx" in response.url.lower():
            for item in self.parse_index(response):
                yield item 
        else:
            for item in self.parse_content(response):
                yield item
        

    def parse_index(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            yield scrapy.Request(url=response.url,callback=self.parse_index)   
            return
        base_url  = get_base_url(response)
 
        #解析期刊首页
        for href in response.xpath('//table/tr/td/a/@href').extract():
            if 'issue_list' not in href  :
                continue

            relative_url = href
            abs_url =urljoin_rfc(base_url,relative_url)
            #yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
            self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)
            yield scrapy.Request(url=abs_url,callback=self.parse_content)

 


    def parse_content(self,response):
        self.log("Crawled %s %d"%(response.url,response.status),level=scrapy.log.INFO)
        #self.log("Crawled (%d) <GET %s>"%(response.status,response.url),level=scrapy.log.INFO)
        if response.status / 100 != 2:
            yield scrapy.Request(url=response.url,callback=self.parse_content)     
            return
        base_url  = get_base_url(response)
        #解析文章
        for href in response.xpath('//table//a/@href').extract():
            if "view_abstract.aspx?"  in href:
                href = url_query_cleaner(href,("file_no"))
            elif"create_pdf.aspx?"  in href:
                pass                
            else:
                continue
            abs_url =urljoin_rfc(base_url,href)            
            yield self.baidu_rpc_request({"url":abs_url,"src_id":22},furl=response.url)
            #self.log("Parse %s %s"%(abs_url,response.url),level=scrapy.log.INFO)



       