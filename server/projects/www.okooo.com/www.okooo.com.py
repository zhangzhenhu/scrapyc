#encoding=gbk
import sys
import lxml.html
import lxml.etree
import pdb
import json
import time
import datetime
import os
import urllib2
import re
import cookielib
import StringIO
import gzip
Start_Time=None
End_Time=None
Sleep_Time=1
M_DB={}
M_QUEUE={}
CHARSET="GB18030"
#cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
urllib2.install_opener(opener)
#httpHandler = urllib2.HTTPHandler(debuglevel=1)
#opener = urllib2.build_opener(httpHandler)
#urllib2.install_opener(opener) 
		
M_COMPANY=[u"竞彩官方",u"威廉.希尔",u"Bet365",u"bwin",u"澳门彩票",u"立博",u"香港马会",u"99家平均"]
#M_COMPANY=[u"竞彩官方",u"99家平均"]
def pget(url):
	#global LAST_GET
        #now=time.time()
        #if now-LAST_GET <2:
        #        time.sleep(1)
        #LAST_GET=now
	re=urllib2.Request(url)
	re.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36")
	#re.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
	re.add_header("Accept-Encoding","gzip,deflate,sdch")
	#re.add_header("Accept-Language","zh-CN,zh;q=0.8,en;q=0.6")
	re.add_header("Host","www.okooo.com")
	re.add_header("Cache-Control","no-cache")
	re.add_header("Pragma","no-cache")
	re.add_header("Connection","keep-alive")
	#pdb.set_trace()
	retry=1
	while retry < 10:
		time.sleep(Sleep_Time)
		try:
			ret=urllib2.urlopen(re,timeout=10)
			if ret.getcode() /100 !=2 :
				print "[wget] failed url:%s retcode:%d" % (url,ret.getcode())
				retry += 1
				time.sleep(Sleep_Time*5)
				continue
			print "[wget] succed url:%s retcode:%d" % (url,ret.getcode())
			reply=ret.info()
			if reply.getheader("Content-Encoding")=="gzip":
				compresseddata = ret.read()
				compressedstream = StringIO.StringIO(compresseddata)
				gzipper = gzip.GzipFile(fileobj=compressedstream)
				
				data=gzipper.read()
				ret.close()
				return  data
			
			data=ret.read()
			ret.close()
			return data
		except  Exception,e:
			print "[wget] error url:%s errcode:%s" % (url,e)
		time.sleep(2)
		retry += 1
	return None


def parse_odds(url):
        #pdb.set_trace()
	global M_DB
	html=pget(url)
	if not html:return
	MatchId=url.split('/')[-4]
	
	tree=lxml.html.fromstring(html.decode("utf8"))
	#table=tree.xpath("//div[@id='data_main_content']/table")[0]
	trs=tree.xpath("tr")
	#if MatchId not in M_DB[day]:
	#	M_DB[day][MatchId]={"odds":{}}
	#data=M_DB[day][MatchId]["odds"]
	data={}
	#pdb.set_trace()
	for tr in trs:
		tds=tr.xpath("td")
		company=unicode(tds[1].text_content()).strip()
		if company not in M_COMPANY:continue
		
		s_zhu=unicode(tds[2].text_content()).strip().replace(u'↓' ,'').replace(u'↑' ,'').strip()
		s_ping=unicode(tds[3].text_content()).strip().replace(u'↓' ,'').replace(u'↑' ,'').strip()
		s_ke=unicode(tds[4].text_content()).strip().replace(u'↓' ,'').replace(u'↑' ,'').strip()
		n_zhu=unicode(tds[5].text_content()).strip().replace(u'↓' ,'').replace(u'↑' ,'').strip()
		n_ping=unicode(tds[6].text_content()).strip().replace(u'↓' ,'').replace(u'↑' ,'').strip()
		n_ke=unicode(tds[7].text_content()).strip().replace(u'↓' ,'').replace(u'↑' ,'').strip()
		href=tds[5].xpath("a/@href")[0]
		#print href
		odds_change=pase_history(href)
		odds_change.update({"company":company,
				"s_zhu":s_zhu,"s_ping":s_ping,"s_ke":s_ke,
				"n_zhu":n_zhu,"n_ping":n_ping,"n_ke":n_ke,})
		data[company]=odds_change
	return data
def pase_history(url,type="odds"):
	html=pget(url)
	if not html:return
	tree=lxml.html.fromstring(html.decode("GB18030"))
	#pdb.set_trace()
	table=tree.xpath("//table")[0]
	trs=table.xpath("tr")[2:]

	zhu_change=""
	ping_change=""
	ke_change=""
	n_zhu_all=""
	#if len(trs) >6:trs=trs[-6:]
	if len(trs)  <= 1:
		return {'zhu_change':zhu_change,'ping_change':ping_change,'ke_change':ke_change}
	c_tr=trs[-1]
	if type=="odds":
		start_pos=2
		end_pos=5
	else:
		start_pos=3
		end_pos=6

	c_zhu,c_ping,c_ke=[e.text_content() for e in c_tr.xpath('td')[start_pos:end_pos]]
	#print c_zhu,c_ping,c_ke
	#if url== "http://www.okooo.com/soccer/match/678362/odds/change/14/":pdb.set_trace()
	for tr in trs[2:-1]:
		tds =  tr.xpath('td')
		if len(tds) < 6:continue
		#pdb.set_trace()
		if u"(终)" in tds[0].text_content():continue
		zhu,ping,ke=[e.text_content() for e in tr.xpath('td')[start_pos:end_pos]]
		if u'↑' in zhu:
			zhu_change = "2" + zhu_change
		elif u'↓' in zhu:
			zhu_change = "0" + zhu_change
		else:
			zhu_change = "1" + zhu_change
		if u'↑' in ping:
			ping_change = "2" + ping_change
		elif u'↓' in ping:
			ping_change = "0" + ping_change
		else:
			ping_change = "1" + ping_change

		if  u'↑' in ke:
			ke_change = "2" + ke_change
		elif u'↓' in ke:
			ke_change = "0" + ke_change
		else:
			ke_change = "1" + ke_change

	return {'zhu_change':zhu_change,'ping_change':ping_change,'ke_change':ke_change}


def parse_hodds(url):
        #pdb.set_trace()
	#global M_DB
	html=pget(url)
	if not html:return {}	
	#MatchId=url.split('/')[-3]
	#pdb.set_trace()
	tree=lxml.html.fromstring(html.decode("utf8"))
	#table=tree.xpath("//div[@id='data_main_content']/table")[0]
	#tree=lxml.html.fromstring(html.decode("GB18030"))
	#table=tree.xpath("//div[@id='datatable1']/table")[0]
	trs=tree.xpath("tr")
	data={}
	avg={}
	count = 0
	s_zhu_all=0
	s_ping_all=0
	s_ke_all=0
	n_ping_all=0
	n_zhu_all=0
	n_ke_all=0
	rangqiu=None
	for tr in trs:
		if tr.get('id') in ['avgObj','maxObj','minObj']:
			continue
		tds=tr.xpath("td")
		company=unicode(tds[1].text_content()).strip()
		value=unicode(tds[2].text_content()).strip()

		if company == u"竞彩官方":
			rangqiu=value
		elif rangqiu != value:
			continue

		s_zhu=unicode(tds[3].text_content()).strip().replace(u'↓' ,'').replace(u'↑' ,'').strip()
		s_ping=unicode(tds[4].text_content()).strip().replace(u'↓' ,'').replace(u'↑' ,'').strip()
		s_ke=unicode(tds[5].text_content()).strip().replace(u'↓' ,'').replace(u'↑' ,'').strip()
		n_zhu=unicode(tds[6].text_content()).strip().replace(u'↓' ,'').replace(u'↑' ,'').strip()
		n_ping=unicode(tds[7].text_content()).strip().replace(u'↓' ,'').replace(u'↑' ,'').strip()
		n_ke=unicode(tds[8].text_content()).strip().replace(u'↓' ,'').replace(u'↑' ,'').strip()
		#pdb.set_trace()
		href=tds[6].xpath("a/@href")[0]
		if company in M_COMPANY:
			if company not in data:data[company]={}
			hodds_change=pase_history(href,"hodds")		
			hodds_change.update({"company":company,"rang":value,
					"s_zhu":s_zhu,"s_ping":s_ping,"s_ke":s_ke,
					"n_zhu":n_zhu,"n_ping":n_ping,"n_ke":n_ke} )
			data[company]=hodds_change
		if value == rangqiu:
			s_zhu_all += float(s_zhu)
			s_ping_all += float(s_ping)
			s_ke_all += float(s_ke)
			n_zhu_all += float(n_zhu.replace(u'↓' ,'').replace(u'↑' ,'').strip())
			n_ping_all += float(n_ping.replace(u'↓' ,'').replace(u'↑' ,'').strip())
			n_ke_all += float(n_ke.replace(u'↓' ,'').replace(u'↑' ,'').strip())
			count +=1
	if count==0:count=1
	data[u"99家平均"]={}	
	data[u"99家平均"]={"company":u"99家平均","rang":rangqiu,
					"s_zhu":int(s_zhu_all*100/count)/100.0,"s_ping":int(100*s_ping_all/count)/100.0,"s_ke":int(100*s_ke_all/count)/100.0,
					"n_zhu":int(100*n_zhu_all/count)/100.0,"n_ping":int(100*n_ping_all/count)/100.0,"n_ke":int(100*n_ke_all/count)/100.0} 
	#print data
	return data

def parse_today(url,html,tday):
	global M_DB
	tree=lxml.html.fromstring(html.decode("GB18030"))
	tables=tree.xpath("//div[@id='gametablesend']//table[@class='jcmaintable']")
	

	for table in tables:
		trs=table.xpath("tr")
		day_src=table.xpath("tr[1]/td/div/span/span")[0].text_content()
		week,day=day_src.strip().split(None,1)
		week=week.strip()
		day=day.strip()
		if day != tday: continue
		#msg=u"%s\t%d条比赛"%(today,len(trs))
		M_DB[day]={}
		#{'week':week}
		#print msg.encode(CHARSET)
		#pdb.set_trace()
		for tr in trs[1:]:
			tds=tr.xpath("td")
			MatchIndex=tds[0].xpath('span/i[1]')[0].text
			MatchName=tds[0].xpath('a[1]')[0].text
			#MatchTime,BuyTime=tds[1].xpath('span/text()')
			MatchTime=tds[1].get("title").split(u"：",1)[1].strip()
			dname1,dname2=tds[2].xpath('a/text()')
			fen=tds[2].xpath('span|b')[0].text_content()
			#print fen
			ou,xi,ao=tds[3].xpath('a/@href')
			MatchId=ou.strip().split('/')[-3]
			
			odds={}
			page=0
			while len(odds)  <  len(M_COMPANY) and page < 10 :
				odds_url="http://www.okooo.com/soccer/match/%s/odds/ajax/?page=%d&companytype=ExceptExchangeMakerID&type=0"%(MatchId,page)
				n_odds=parse_odds(odds_url)
				page +=1 
				odds.update(n_odds)

			
			hodds_url="http://www.okooo.com/soccer/match/%s/hodds/ajax/?page=%d&companytype=&type=0"%(MatchId,page)
			hodds=parse_hodds(hodds_url)
			

			M_DB[day][MatchId]={'m_index':MatchIndex,'m_id':MatchId, 'm_name':MatchName,'m_time':MatchTime,'buy_time':"",'dname1':dname1,'dname2':dname2,"fen":fen,"odds":odds,"hodds":hodds}

			continue

	return 

def main():
	#pdb.set_trace()
	global Start_Time,End_Time,M_QUEUE,M_DB
	start=Start_Time
	while start <= End_Time:
		if start.isoformat()  not in M_DB:

			url='http://www.okooo.com/jingcai/shengpingfu/%s/'%start.isoformat()
			html = pget(url)
			if not html:
				return False
			parse_today(url,html,start.isoformat())
			if Need_Dump:
				dump_data()
		start= start+datetime.timedelta(1)
	#print M_DB
	print
	print
	return True


def print_data():
	global M_DB	
	for day ,sai  in  M_DB.items():
		print day.encode(CHARSET)
		for MatchId,MatchData in sai.items():
			#print MatchData	
			MatchName=MatchData["m_name"]
			MatchTime=MatchData["m_time"]
			BuyTime=MatchData["buy_time"]
			dname1=MatchData['dname1']
			dname2=MatchData['dname2']
			fen = MatchData['fen']
			msg=u"赛事:%-5s\t比赛时间:%s\t投注截止时间:%s\t参赛队:%s\t%s\t%s"%(MatchName,MatchTime,BuyTime,dname1,fen,dname2,)
			print msg.encode(CHARSET)
			msg=u"  %25s\t%22s\t%30s"%(u"公司",u"初始指数",u"终止指数")
			print msg.encode(CHARSET)
			odds_data=MatchData["odds"]
			for item in odds_data.values()[:5]:
				msg=u" [欧赔]公司:%-20s\t     主: %-5s平: %-5s客: %-5s"%(item["company"],item["s_zhu"],item["s_ping"],item["s_ke"])
				print msg.encode(CHARSET)

			print 
			hodds_data=MatchData["hodds"]

			for items in hodds_data.values()[:5]:
				for rang,item in items.items():
					msg=u" [让球]公司:%-20s\t%-5s主:%-5.4s平:%-5.4s客:%-5.4s"%(item["company"],rang,item["s_zhu"],item["s_ping"],item["s_ke"])
					print msg.encode(CHARSET)			
			print


def jud(t1,t2,t3):

	if len(t1) > 5:
		t1=t1[:5]
	if len(t2) > 5:
		t2=t2[:5]
	if len(t3) > 5:
		t3=t3[:5]

	for i in t1,t2,t3:
		if i != "1":
			return t1,t2,t3
	return "","",""
		
def make_excel():
	import xlwt
	global M_COMPANY
	Weeks=[u"星期一",u"星期二",u"星期三",u"星期四",u"星期五",u"星期六",u"星期日",]
	book=xlwt.Workbook(encoding=CHARSET)
	excel={}
	for company in M_COMPANY[:-1]:
		sheet=book.add_sheet(company.encode(CHARSET))
		sheet.write_merge(0,1,0,0,u"场次")
		sheet.write_merge(0,1,1,1,u"比赛筛选")
		sheet.write_merge(0,1,2,2,u"比赛时间")
		sheet.write_merge(0,1,3,3,u"主队")
		sheet.write_merge(0,1,4,4,u"客队")
		sheet.write_merge(0,1,5,5,u"比分")
		sheet.write_merge(0,1,6,6,u"彩果")
		sheet.write_merge(0,1,7,7,u"让球")
		sheet.write_merge(0,1,8,8,u"让球彩果")
		sheet.write_merge(0,0,9,26,company)
		sheet.write_merge(1,1,9,11,u"胜平负初赔")
		sheet.write_merge(1,1,12,14,u"胜平负终赔")
		sheet.write_merge(1,1,15,17,u"让球初赔")
		sheet.write_merge(1,1,18,20,u"让球终赔")
		sheet.write_merge(1,1,21,23,u"胜平负即时变化")
		sheet.write_merge(1,1,24,26,u"让球即时变化")
		sheet.write_merge(0,0,27,38,u"99家平均赔率")
		sheet.write_merge(1,1,27,29,u"胜平负初赔")
		sheet.write_merge(1,1,30,32,u"胜平负终赔")
		sheet.write_merge(1,1,33,35,u"让球初赔")
		sheet.write_merge(1,1,36,38,u"让球终赔")
		excel[company]=sheet
	row=0#这里必须是1
	#取出一场赛事
	Days=M_DB.keys()
	Days.sort()
	global Start_Time,End_Time
	#start=Start_Time
	#while start <= End_Time:	
	for day  in Days :
		value=[ int(i) for i in day.strip().split('-')]
		cday=datetime.date(*value )
		if cday >= Start_Time and cday <= End_Time:
			pass
		else:
			continue
		sai=M_DB[day]
		print day.encode(CHARSET)
		value=[ int(i) for i in day.strip().split('-')]
		week=Weeks[datetime.date(*value ).weekday()]
		row +=1
		count=0
		#写入一场比赛信息
		MatchDatas=sorted(sai.values(),key=lambda d:d["m_index"])
		
		for MatchData in MatchDatas:
			row += 1
			count +=1
			#print MatchData	
			MatchIndex=MatchData["m_index"]
			MatchId =MatchData["m_id"]
			MatchName=MatchData["m_name"]
			MatchTime=MatchData["m_time"]
			BuyTime=MatchData["buy_time"]
			dname1=MatchData['dname1']
			dname2=MatchData['dname2']
			fen = MatchData['fen']
			msg=u"赛事:%-5s\t比赛时间:%s\t投注截止时间:%s\t参赛队:%s\t%s\t%s"%(MatchName,MatchTime,BuyTime,dname1,fen,dname2,)
			print msg.encode(CHARSET)
			#msg=u"  %25s\t%22s\t%30s"%(u"公司",u"初始指数",u"终止指数")
			#print msg.encode(CHARSET)
			
			#此场比赛的欧赔数据 字典类型 key是公司名
			odds_data=MatchData["odds"]
			#此场比赛的让陪数据 字典类型 key是公司名
			hodds_data=MatchData["hodds"]
			#pdb.set_trace()
			#取出平均数据 
			if u"99家平均"  in odds_data:
				AVG99_odds=odds_data[u"99家平均" ]
			else:
				AVG99_odds={}

			if u"99家平均"  in hodds_data:
				AVG99_hodds=hodds_data[u"99家平均" ]
			else:
				AVG99_hodds={}

			#写入此场赛事的各个公司的赔率信息
			#从第三行开始写（从0起算）
			
			for company in M_COMPANY: #odds_data.values():#此场比赛的欧赔数据 字典类型 key是公司名

				
				if company  == u"99家平均":
					continue
				if company in odds_data:
					item=odds_data[company]
				else:
					item={}

				if company in hodds_data:
					rang_data=hodds_data[company]
				else:
					rang_data={}

				#取出此公司对应的sheet表格
				sheet=excel[company]
				
				col=0				
				sheet.write(row,0,u"%s %s %s"%(day,week,MatchIndex))

				#写入比赛信息
				sheet.write(row,1,MatchName)
				sheet.write(row,2,MatchTime)
				sheet.write(row,3,dname1)
				sheet.write(row,4,dname2)
				sheet.write(row,5,fen)
				sheet.write(row,6,caiguo(fen))
				if 'rang'  in rang_data:
					rangqiu=rang_data['rang']
				else:
					rangqiu=0
				sheet.write(row,7,rangqiu)
				sheet.write(row,8,caiguo(fen,int(rangqiu)))
				if item:
					#写入公司的胜平负初赔
					sheet.write(row,9,item["s_zhu"])
					sheet.write(row,10,item["s_ping"])
					sheet.write(row,11,item["s_ke"])
					#写入公司的胜平负终赔
					sheet.write(row,12,item["n_zhu"])
					sheet.write(row,13,item["n_ping"])
					sheet.write(row,14,item["n_ke"])
					#写入公司的胜平负及时变化
					t1,t2,t3 = jud(item["zhu_change"],item["ping_change"],item["ke_change"])
					sheet.write(row,21,t1)
					sheet.write(row,22,t2)
					sheet.write(row,23,t3)
				if rang_data:
					#写入公司的让球初赔
					sheet.write(row,15,rang_data["s_zhu"])
					sheet.write(row,16,rang_data["s_ping"])
					sheet.write(row,17,rang_data["s_ke"])
					#写入公司的让球终赔
					sheet.write(row,18,rang_data["n_zhu"])
					sheet.write(row,19,rang_data["n_ping"])
					sheet.write(row,20,rang_data["n_ke"])

					t1,t2,t3 = jud(rang_data["zhu_change"],rang_data["ping_change"],rang_data["ke_change"])
					#写入公司的胜平负及时变化
					sheet.write(row,24,t1)
					sheet.write(row,25,t2)
					sheet.write(row,26,t3)

				if AVG99_odds:

					#写入平均的胜平负初赔
					sheet.write(row,27,AVG99_odds["s_zhu"])
					sheet.write(row,28,AVG99_odds["s_ping"])
					sheet.write(row,29,AVG99_odds["s_ke"])
					#写入平均的胜平负终赔
					sheet.write(row,30,AVG99_odds["n_zhu"])
					sheet.write(row,31,AVG99_odds["n_ping"])
					sheet.write(row,32,AVG99_odds["n_ke"])

				if AVG99_hodds:

					#写入平均的让球初赔
					sheet.write(row,33,AVG99_hodds["s_zhu"])
					sheet.write(row,34,AVG99_hodds["s_ping"])
					sheet.write(row,35,AVG99_hodds["s_ke"])
					#写入平均的让球终赔
					sheet.write(row,36,AVG99_hodds["n_zhu"])
					sheet.write(row,37,AVG99_hodds["n_ping"])
					sheet.write(row,38,AVG99_hodds["n_ke"])
				
				#msg=u" [欧赔]公司:%-20s\t     主: %-5s平: %-5s客: %-5s"%(item["company"],item["s_zhu"],item["s_ping"],item["s_ke"])
				#print msg.encode(CHARSET)

			print 
	

	
	if Start_Time==End_Time:
		book.save(u"%s.xls"%Start_Time.isoformat())
	else:
		book.save(u"%s到%s.xls"%(Start_Time.isoformat(),End_Time.isoformat()))
def caiguo(fen_str,rang=0):
	if fen_str=="VS":return ""
	a,b=fen_str.split("-")
	a=int(a)+int(rang)
	b=int(b)
	c=a-b
	if c<0:return 0
	if c==0:return 1
	if c>0:return 3

def print_help():
	global CHARSET
	print u"用法示例：".encode(CHARSET)
	print u"python www.okooo.com.py  -s 开始日期 -e 结束日期  -t 抓取间隔秒数".encode(CHARSET)
	print  u"注意抓取的太快会被网站封禁，默认抓取间隔1秒。友情提示：个人测试小于1秒就会被封杀".encode(CHARSET)
	print 
	print u"抓取当天的数据：".encode(CHARSET)
	print u"python www.okooo.com.py  ".encode(CHARSET)
	print
	print u"抓取指定日期的数据：".encode(CHARSET)
	print  u"python www.okooo.com.py  -s 2014-10-12 -e 2014-10-14 ".encode(CHARSET)
	print  " "

import getopt
import json
Need_Dump=False
def dump_data():
	try:
		f=open("db.json",'w')
		json.dump(M_DB,f,encoding=CHARSET)
		f.close()
	except Exception, e:
		print e
if __name__ == "__main__":
	#pget('http://www.okooo.com/soccer/match/644183/hodds/ajax/?page=1&companytype=&type=0')
	#print pase_history("http://www.okooo.com/soccer/match/709890/odds/change/14/","odds")
	#sys.exit()
	if len(sys.argv) > 1:
		try:
			options,args = getopt.getopt(sys.argv[1:],"hs:e:t:",["help",])
			for name,value in options:
				if name == "-s":
					value=[ int(i) for i in value.strip().split('-')]
					Start_Time=datetime.date(*value )
							
				if name == "-e":
					value=[ int(i) for i in value.strip().split('-')]
					End_Time=datetime.date(*value )
				if name == "-t":
					Sleep_Time=float(value)
				if name == "-h":
					print_help()
					sys.exit()					

		except getopt.GetoptError:
			print_help()
			sys.exit()

	print_help()	
		

	if not Start_Time:
		Start_Time=datetime.date.today()
	if not End_Time:
		End_Time=datetime.date.today()
	if datetime.date.today() > End_Time:
		try:
			Need_Dump=True
			f=open("db.json","r")
			M_DB=json.load(f,encoding=CHARSET)
			f.close()

		except:
			pass
	if not main():
		sys.exit(1)
#
	if Need_Dump:
		dump_data()

	make_excel()
