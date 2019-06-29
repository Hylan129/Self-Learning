import pymssql
import xlwt
import datetime
import random
 
conn=pymssql.connect(host='FH7ZI2B38ALDODR',user='',password='',database='DatabaseSQLRobot',charset='utf8')
#conn=pymssql.connect(host='FH7ZI2B38ALDODR',user='',password='qxznqipai!',database='DatabaseSQLRobot',charset='utf8')
cursor =conn.cursor()
if not cursor:
    raise(NameError,"连接数据库失败")
else:
    print("It's succeed for database connect !")

#查询
sql_content_0 = "SELECT * FROM "

#删除
sql11 = """ DELETE FROM Equip WHERE equip_no>200 """
#插入
sql12 = """INSERT INTO SetParm(sta_n, equip_no, set_no, set_nm, 
	set_type, main_instruction, minor_instruction, record, action, value, canexecution, 
	VoiceKeys, EnableVoice, Reserve1, Reserve2, Reserve3) 
	VALUES (1, 1, 1290, 'Hylan', 'X', 'Move', '0', 'True', '设置', '0.5', 'True', '', 'False', '回家了', '', '')"""
#更新
sql13 = """UPDATE  SetParm
		SET	set_nm = '测试结果'
		WHERE   (set_no = 1290)"""
		
title_list =['QXRobotVoice','SetParm','Equip','yxp','ycp','AutoProc']

#查字段名
sql_title_0 = "SELECT name FROM   syscolumns WHERE  id = Object_id('"

sql_title_2 = "') Order by colid"


"""
cursor.execute(sql)
conn.commit()
cursor.execute("SELECT set_nm FROM SetParm WHERE (set_no = 1290)")
"""

myWorkbook = xlwt.Workbook()

for list in range(len(title_list)):
	
	table_name = title_list[list]
	
	mySheet = myWorkbook.add_sheet(table_name)

	sql1 = sql_title_0 + table_name +sql_title_2

	#print(sql1)

	cursor.execute(sql1)
	
	titles = cursor.fetchall()

	for number in range(len(titles)):
		mySheet.write(0,number,titles[number][0])

	sql2 = sql_content_0 + table_name

	# 执行SQL语句
	cursor.execute(sql2)
	# 获取所有记录列表
	results = cursor.fetchall()

	row_QXRobotVoice = len(results)
	number_row = len(results[0])
	#print(row_QXRobotVoice,number_row)

	for row in range(row_QXRobotVoice):
		for number in range(number_row):
			mySheet.write(row+1,number,results[row][number])
			
#myWorkbook.save('backup.xls') 
xlsfile_text1 = datetime.datetime.now().strftime('%Y-%m-%d')
xlsfile_text2 = random.randint(1,99)

#通过sheet_by_index()获取的sheet没有write()方法
myWorkbook.save('database backup_'+ xlsfile_text1 +'_'+ str(xlsfile_text2) + '.xls') 
"""
try:
   # 执行SQL语句
	cursor.execute(sql)
   # 获取所有记录列表
	results = cursor.fetchall()
	
	row_QXRobotVoice = len(results)
	print(row_QXRobotVoice)
	for row in range(row_QXRobotVoice):
		for number in range(len(results[row])):
			mySheet.write(row,0,results[row][0])
			mySheet.write(row,1,results[row][1])
			mySheet.write(row,2,results[row][2])
			
	myWorkbook.save('backup.xls') 
except:
	print("Error: unable to fecth data")
"""
