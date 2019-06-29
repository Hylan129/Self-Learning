import xlrd
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy 
import datetime
import random

#txt = open(r'C:\Users\Administrator\Desktop\txt\Debug.txt').read()

txt = open(r'Debug.txt').read()

matchcount = len(txt.split("匹配关键词"))-1

txt_Split = txt.split('**********************************************************************************************')
'''
 *******************************************2019年4月18日-9:50:15(服务端)*******************************************
设备号：6---设备名：六麦语音
 说话内容：往前走，匹配关键词：向or往or朝%前%走or动or行or挪,回复内容：好的,当前标识：A,marked:A，执行:
'''
'''
 time : txt[1][44:62]
 device_number : txt[1][115:116]
 device_name :  txt[1][122:127]
 说话内容：txt[1][133:1000].split('，')[0] //需要判断是否有匹配关键词
 
 匹配关键词：txt[1].split('匹配关键词：')[1].split(',')[0] //需要判断是否有匹配关键词
 回复内容：txt[1].split('回复内容：')[1].split(',')[0] //需要判断是否有匹配关键词
  
'''
count = len(txt_Split)-1

myWorkbook = xlwt.Workbook()
mySheet = myWorkbook.add_sheet('Record_List')
mySheet.col(1).width = 256 * 25
mySheet.col(2).width = 256 * 15
mySheet.col(3).width = 256 * 15
mySheet.col(4).width = 256 * 15
mySheet.col(5).width = 256 * 30
mySheet.col(7).width = 256 * 20

myStyle0 = xlwt.easyxf("font: height 300,name Times New Roman, color-index red, bold on;align: wrap on, vert centre, horiz centre;")
myStyle_centre = xlwt.easyxf("align: wrap on, vert centre, horiz centre;")
myStyle = xlwt.easyxf('font: name Times New Roman, color-index red, bold on;align: wrap on, vert centre, horiz centre;', num_format_str='0.0%')

mySheet.write_merge(0, 1,0,7,"小π机器人语音测试反馈记录表",myStyle0)
#myStyle = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')


mySheet.write(2,0,"起始时间",myStyle_centre)
mySheet.write(2,1,txt_Split[0].split('*******************************************')[1].split('(')[0],myStyle_centre)
mySheet.write(3,0,"结束时间",myStyle_centre)
mySheet.write(3,1,txt_Split[count-1].split('*******************************************')[1].split('(')[0],myStyle_centre)

mySheet.write(2,2,"识别次数",myStyle_centre)
mySheet.write(2,3,count,myStyle_centre)
mySheet.write(3,2,"匹配次数",myStyle_centre)
mySheet.write(3,3,matchcount,myStyle_centre)

mySheet.write(2,4,"匹配率",myStyle_centre)
mySheet.write(2,5,matchcount/count,myStyle)


mySheet.write(5,0,"No.")
mySheet.write(5,1,"识别时间")
mySheet.write(5,2,"机器人设备号")
mySheet.write(5,3,"机器人设备名称")
mySheet.write(5,4,"识别语音内容")
mySheet.write(5,5,"匹配关键词")
mySheet.write(5,6,"回复内容")
mySheet.write(5,7,"备注说明")

for i in range(6,count+6):
	if(i==6):	
		mySheet.write(i,0,i-5)
		mySheet.write(i,1,txt_Split[i-6].split('*******************************************')[1].split('(')[0])
		mySheet.write(i,2,txt_Split[i-6].split('设备号：')[1].split('-')[0])
		mySheet.write(i,3,txt_Split[i-6].split('设备名：')[1].split()[0])
		judge_txt = txt_Split[i-6]
		if('说话内容：' in judge_txt):
			if('匹配关键词' in judge_txt):
				mySheet.write(i,4,txt_Split[i-6].split('说话内容：')[1].split('，')[0])
				mySheet.write(i,5,txt_Split[i-6].split('匹配关键词：')[1].split(',')[0])
				mySheet.write(i,6,txt_Split[i-6].split('回复内容：')[1].split(',')[0])
				mySheet.write(i,7,'已匹配到！')
			else:
				print(judge_txt)
				mySheet.write(i,4,txt_Split[i-6].split('说话内容：')[1].split(',')[0])
			
				mySheet.write(i,7,txt_Split[i-6].split('说话内容：')[1].split(',')[1])
		else:
			
			mySheet.write(i,7,'信息异常！未识别到说话声！')
			
	else:
		mySheet.write(i,0,i-5)
		mySheet.write(i,1,txt_Split[i-6].split('*******************************************')[1].split('(')[0])
		mySheet.write(i,2,txt_Split[i-6].split('设备号：')[1].split('-')[0])
		#mySheet.write(i,2,txt_Split[i-6][115:116])
		mySheet.write(i,3,txt_Split[i-6].split('设备名：')[1].split()[0])
		#mySheet.write(i,3,txt_Split[i-6][123:128])
		judge_txt = txt_Split[i-6]
		if('说话内容：' in judge_txt):
			if('匹配关键词' in judge_txt):
				mySheet.write(i,4,txt_Split[i-6].split('说话内容：')[1].split('，')[0])
				mySheet.write(i,5,txt_Split[i-6].split('匹配关键词：')[1].split(',')[0])
				mySheet.write(i,6,txt_Split[i-6].split('回复内容：')[1].split(',')[0])
				mySheet.write(i,7,'已匹配到！')
			else:
				#print(judge_txt)
				mySheet.write(i,4,txt_Split[i-6].split('说话内容：')[1].split(',')[0])
			
				mySheet.write(i,7,txt_Split[i-6].split('说话内容：')[1].split(',')[1])
		else:
			
			mySheet.write(i,7,'信息异常！未识别到说话声！')
			
xlsfile_text1 = datetime.datetime.now().strftime('%Y-%m-%d')
xlsfile_text2 = random.randint(1,99)

#通过sheet_by_index()获取的sheet没有write()方法
myWorkbook.save('Debug_Analysis_'+ xlsfile_text1 +'_'+ str(xlsfile_text2) + '.xls') 
