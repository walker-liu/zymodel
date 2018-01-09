﻿#encoding:utf-8
'''由于文件较大，需要读取一行处理一行，直接写进文件中
'''
import xlwt
import xlsxwriter
import re
def proLine(line):
	#print line
	tmp=line.replace(u'：',u':').split(u'|')
	date=tmp[0]
	province=tmp[2]
	city=tmp[4]
	work_order=tmp[5]
	sent=''.join(tmp[6:])
	#sent为剩余要处理的文本
	#首先对sent以";"进行切分
	#然后对切分后的每一个元素以":"进行切割，可以得到[方面：具体内容]
	w_tmp=sent.split(u';')
	aspects=[]
	contents=[]
	for w in w_tmp:
		#print w
		if ':' in w:
			ind=w.index(u':')
			aspects.append(w[:ind])
			contents.append(w[ind+1:])
		else:
			pass
	return date,province,city,work_order,aspects,contents
		
def process(src,res):
	wb=xlsxwriter.Workbook(res)
	#wt=xlwt.Workbook()
	#ws=wt.add_sheet('sheet')
	ws=wb.add_worksheet(u'sheet1')
	num=1
	ws.write(0,0,u"日期")
	ws.write(0,1,u"省份")
	ws.write(0,2,u"城市")
	ws.write(0,3,u"工单号")
	ws.write(0,4,u"模板")
	#ws.write(0,5,"内容")
	
	with open(src,'r') as f_r:
		for line in f_r:
			line=line.decode('utf-8').strip()
			if line:
				data=proLine(line)
				ws.write(num,0,data[0])
				ws.write(num,1,data[1])
				ws.write(num,2,data[2])
				ws.write(num,3,data[3])
				ws.write(num,4,u'.*'.join(data[4])+u'.*')
				num+=1
	#wt.save(res)
	wb.close()
	
def choose(model,src,res,res2):
	flag=True
	flag_model=True
	with open(res2,'w') as f_w2:
		with open(res,'w') as f_w:
			with open(src,'r') as f_r:
				for line in f_r:
					line=line.decode('utf-8').strip()
					if line:
						#if u':' in line:
						if u'' in line:
							tmp=line.split(':')
							if len(tmp)>3:
								for w in model:
									pattern=re.compile(w)
									match = pattern.match(line)
									if match:
										flag_model=False
										break
								if flag_model==True:
									f_w.write((line+'\n').encode('utf-8'))
								else:
									flag_model=True									
							else:
								#f_w2.write((line+'\n').encode('utf-8'))
								f_w.write((line+'\n').encode('utf-8'))
								pass
						elif u';' in line:
							tmp=line.split(';')
							if len(tmp)>3:
								for w in model:
									pattern=re.compile(w)
									match = pattern.match(line)
									if match:
										flag_model=False
										break
								if flag_model==True:
									f_w.write((line+'\n').encode('utf-8'))
								else:
									flag_model=True	
							else:
								#f_w2.write((line+'\n').encode('utf-8'))
								f_w.write((line+'\n').encode('utf-8'))
								pass
						else:
							#f_w2.write((line+'\n').encode('utf-8'))
							f_w.write((line+'\n').encode('utf-8'))
							pass
model=[
	u'.*1 、故障时间.*故障号码为.*2 、故障现象为.*3 、是否曾欠费停机.*4 、周围人是否使用正常.*5 、故障地点为.*6 、是否个别网站/第三方应用无法使用.*7 、其他为.*客户要求.*',
	u'.*主活动名称:.*主活动ID:.*子活动名称:.*操作员组织:.*操作员工号:.*操作员:.*渠道类型:.*办理时间:.*反映.*',
	u'.*1、.*家庭宽带客户:.*2、设备信息：.*3、联系电话：.*4、故障地点：.*5、预处理内容：.*结果:.*客户要求：.*',
	u'.*1、.*家庭宽带客户:.*2、设备信息：.*3、联系电话：.*4、故障地点：.*5、预处理内容：.*',
	u'.*1 、故障开始时间为.*2 、故障现象为.*3 、手机4G上网是否正常(或是否在所有地点均不好用).*4 、多次重启设备是否恢复.*5 、故障地点.*6 、是否个别网站/第三方应用无法使用（选是时填写网站或软件名）.*7 、其他.*客户要求.*',
	u'.*1 、故障开始时间.*2 、故障现象.*3 、手机4G上网是否正常(或是否在所有地点均不好用).*4 、故障地点.*5 、是否个别网站/第三方应用无法使用（选是时填写网站或软件名）.*6 、其他.*客户要求.*',
	u'.*1 、故障类型.*2 、故障开始时间.*3 、故障号码.*4 、周围人是否使用正常（关开4G开关或更换手机是否正常）.*5 、故障地点.*6 、其他信息及客户要求.*',
	u'.*1 、故障开始时间.*2 、故障现象.*3 、手机4G上网是否正常(或是否在所有地点均不好用).*4 、故障地点.*5 、是否个别网站/第三方应用无法使用（选是时填写网站或软件名）.*6 、其他.*客户要求.*',
	u'.*该客户通过服务质量监督电话申诉，.*',
	u'.*主活动名称:.*主活动ID:.*子活动名称:.*操作员组织:.*操作员工号:.*渠道类型:.*办理时间:.*',
	u'.*1 、故障开始时间.*2 、故障现象.*3 、多次重启设备.*4 、故障地点.*5 、是否个别网站/第三方应用无法使用（选是时填写网站或软件名）.*6 、其他.*客户要求.*',	u'.*【客户信息】客户编号:.*客户名称:.*集团级别:.*客户服务等级:.*集团客户经理联系人:.*集团客户经理联系电话:.*客户经理:.*客户经理电话:.*客户区域所在城市:.*所在区县:.*产品实例标识:.*业务保障等级:.*业务服务时限:.*业务类型:.*【投诉现象】:.*投诉人信息】回复号码:.*客户联系电话:.*【处理建议流程】.*',
	u'.*1 、故障开始时间.*2 、故障现象.*3 、手机4G上网是否正常(或是否在所有地点均不好用).*4 、其他.*客户要求.*',
	u'.*1 、故障开始时间.*2 、故障现象.*3 、手机4G上网是否正常(或是否在所有地点均不好用).*4 、故障地点.*5 、是否个别网站/第三方应用无法使用（选是时填写网站或软件名）.*6 、其他.*客户要求.*',
	u'.*1 、故障开始时间.*2 、故障现象.*3 、手机4G上网是否正常(或是否在所有地点均不好用).*4 、故障地点.*5 、是否个别网站/第三方应用无法使用（选是时填写网站或软件名）.*',
	u'.*1 、故障时间.*2 、故障号码.*3 、故障现象.*4 、其他信息及客户要求.*',
	u'.*1 、故障开始时间.*2 、故障现象.*',
	u'.*1 、主叫号码.*2 、故障现象.*3 、故障开始时间.*4 、故障结束时间.*5 、其他信息及客户要求.*',
	u'.*1 、短信发送方是否为本省客户.*2 、被叫号码.*3 、不能接收的短信类型.*4 、故障开始时间.*5 、故障结束时间.*6 、其他信息及客户要求.*网络信息诊断结果：.*',
	u'.*1 、故障时间.*故障号码.*2 、周围人是否使用正常.*3 、故障地点.*4 、其他.*客户要求.*',
	u'.*1 、故障时间.*2 、选择具体提示音.*3 、故障号码.*4 、主叫客户故障所在位置.*5 、被叫客户故障所在位置.*6 、主被叫号码更换终端后是否正常.*7 、其他信息及客户要求.*',
	u'.*1、主叫号码.*2、故障现象：.*3、故障开始时间：.*4、故障结束时间：.*5、其他信息及客户要求：.*网络信息诊断结果：.*',
	u'.*1 、故障类型.*2 、故障开始时间.*3 、故障号码.*4 、周围人是否使用正常（或更换手机是否正常）.*5 、是否与单一用户不好用，与其他用户通话正常（如提示正在通话中或忙音）.*6 、故障地点.*7 、对方号码.*8 、其他信息及客户要求.*',
	u'.*1 、故障开始时间.*2 、其他.*客户要求.*',
	u'.*1 、故障时间.*2 、故障现象.*3 、是否曾欠费停机（故障时间3天内）.*4 、周围人是否使用正常（关开4G开关或更换手机是否正常）.*5 、故障地点.*6 、其他.*客户要求.*',
	u'.*1 、故障时间.*2 、选择具体提示音.*3 、故障号码.*4 、主叫客户故障所在位置.*5 、其他信息及客户要求.*',
	u'.*1 、故障时间.*2 、故障现象.*3 、是否曾欠费停机（故障时间3天内）.*4 、周围人是否使用正常（关开4G开关或更换手机是否正常）.*5 、故障地点.*6 、是否个别网站/第三方应用无法使用（选是时填写网站或软件名）.*7 、其他.*',
	u'.*1 、故障时间.*2 、其他.*客户要求.*',	u'.*1、故障时间.*2、故障现象.*3、是否曾欠费停机（故障时间3天内）.*4、周围人是否使用正常（关开4G开关或更换手机是否正常）.*5、故障地点.*6、是否个别网站/第三方应用无法使用（选是时填写网站或软件名）.*7、其他.*8、已登记到数据网络，登记MME地址.*网络信息系统诊断结果.*',
	u'.*未经客户许可情况下被办理.*客户要求.*',
	u'.*客户为品牌内包含.*本地流量.*没有超出赠送流量却产生.*',	u'.*1、故障类型.*2、故障开始时间.*3、故障号码.*4、周围人是否使用正常（关开4G开关或更换手机是否正常）.*5、故障地点.*6、显示信号（2G/3G/4G/G/E/T/H/LTE）.*7、其他信息及客户要求.*',	u'.*1、短信发送方是否为本省客户.*2、被叫号码.*3、不能接收的短信类型.*4、被叫号码.*5、故障开始时间.*6、故障结束时间.*7、其他信息及客户要求.*',
	u'.*1、主叫号码.*2、故障现象.*3、故障开始时间.*4、故障结束时间.*5、其他信息及客户要求.*',	u'.*1、故障时间.*2、故障现象.*3、是否曾欠费停机（故障时间3天内）.*4、周围人是否使用正常（关开4G开关或更换手机是否正常）.*5、其他.*',
	u'.*集团热线投诉客户，请尽快处理客户名字.*客户否认号码.*客户证件号.*客户联系电话.*如打不开附件，请联系我处我处电话.*',	u'.*1、故障时间.*2、故障现象.*3、是否曾欠费停机（故障时间3天内）.*4、周围人是否使用正常（关开4G开关或更换手机是否正常）.*5、故障地点.*6、是否个别网站/第三方应用无法使用（选是时填写网站或软件名）.*7、其他.*',
	u'.*1、故障时间.*2、未登记到数据网络.*',	u'.*1、故障类型.*2、故障开始时间.*3、故障号码.*4、周围人是否使用正常（关开4G开关或更换手机是否正常）.*5、故障地点.*6、其他信息及客户要求.*',
	u'.*1 、故障类型.*2 、故障开始时间.*3 、故障号码.*4 、周围人是否使用正常（或更换手机是否正常）.*5 、是否与单一用户不好用，与其他用户通话正常（如提示正在通话中或忙音）.*6 、故障地点.*7 、其他信息及客户要求.*8 、是否漫游为否.*',
	u'.*1 、故障类型.*2 、故障开始时间.*3 、故障号码.*4 、周围人是否使用正常（关开4G开关或更换手机是否正常）.*5 、其他信息及客户要求.*',	u'.*1、故障类型.*2、故障开始时间.*3、故障号码.*4、周围人是否使用正常（关开4G开关或更换手机是否正常）.*5、故障地点.*6、今天出现几次这种现象.*7、对方号码.*8、其他信息及客户要求.*',
	u'.*1、故障类型.*2、故障开始时间.*3、故障号码.*4、周围人是否使用正常（或更换手机是否正常）.*5、其他信息及客户要求.*',	u'.*1、故障类型.*2、故障开始时间.*3、故障号码.*4、周围人是否使用正常（或更换手机是否正常）.*5、是否与单一用户不好用，与其他用户通话正常（如提示正在通话中或忙音）.*6、故障地点.*',
	u'.*1 、故障时间.*2 、选择具体提示音.*3 、故障号码.*4 、其他信息及客户要求.*',	u'.*1、故障时间.*2、故障现象.*3、是否曾欠费停机（故障时间3天内）.*4、重启手机后是否正常.*5、周围人是否使用正常（关开4G开关或更换手机是否正常）.*6、故障地点.*7、是否个别网站/第三方应用无法使用（选是时填写网站或软件名）.*8、其他.*',	u'.*1、主叫是否为本省客户.*2、被叫号码.*3、主叫号码.*4、被叫号码.*5、故障开始时间.*6、故障结束时间.*7、其他信息及客户要求.*',
	u'.*1 、故障开始时间.*2 、故障现象.*3 、手机4G上网是否正常(或是否在所有地点均不好用).*',
	u'.*故障开始时间.*故障现象.*'
		]
if __name__=='__main__':
	import sys
	#process(sys.argv[1].decode('gbk'),sys.argv[2].decode('gbk'))
	choose(model,sys.argv[1].decode('gbk'),sys.argv[2].decode('gbk'),sys.argv[3].decode('gbk'))
	
				
				
				
				