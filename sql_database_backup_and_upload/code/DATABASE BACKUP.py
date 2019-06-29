import pymssql
import xlwt
import datetime
import configparser

config = configparser.ConfigParser()
try:
	config.readfp(open(r'setting.ini'))
	host_set = config.get("sql_setting","host")
	user_set = config.get("sql_setting","user")
	password_set = config.get("sql_setting","password")
	database_set = config.get("sql_setting","database")

	title_list = config.get("sql_setting","table_down").split('|')
except:
	print("\n数据库连接setting配置文件异常，请检查setting.ini文件！\n")
else:
	#查字段名
	sql_title_0 = "SELECT name FROM   syscolumns WHERE  id = Object_id('"
	sql_title_2 = "') Order by colid"
	sql_content_0 = "SELECT * FROM "
	#数据库连接
	try:
		conn=pymssql.connect(host=host_set,user=user_set,password=password_set,database=database_set,charset='utf8')
		cursor =conn.cursor()
	except Exception as e:
		print(e)
	if not cursor:
		raise(NameError,"连接数据库失败!请检查sett参数配置！")
		print("连接异常！")
	else:
		print("\n\n %s 数据库连接成功！\n"% database_set )

		#数据库备份

		myWorkbook = xlwt.Workbook()
		
		down_count = 0

		for list in range(len(title_list)):
			
			table_name = title_list[list]
			
			mySheet = myWorkbook.add_sheet(table_name)

			sql1 = sql_title_0 + table_name +sql_title_2

			try:
				cursor.execute(sql1)
			except:
				print("数据表%s 在数据库中不存在！\n\n" % table_name)
			else:
			
				titles = cursor.fetchall()
				
				#写字段名第一行
				for number in range(len(titles)):
					mySheet.write(0,number,titles[number][0])

				sql2 = sql_content_0 + table_name
				
				try:
					# 执行SQL语句
					cursor.execute(sql2)
				except:
					print("数据表%s 在数据库中不存在！\n\n" % table_name)
				else:
					# 获取所有记录列表
					results = cursor.fetchall()

					row_QXRobotVoice = len(results)
					number_row = len(results[0])
					#print(row_QXRobotVoice,number_row)

					for row in range(row_QXRobotVoice):
						for number in range(number_row):
							mySheet.write(row+1,number,results[row][number])
				
					print("## 数据表 %s 下载成功！\n" % table_name)
					
					down_count = down_count + 1
					
		print("全部数据表已经下载。需求下载：%d 个数据表，实际下载：%d 个数据表！\n" % (len(title_list),down_count))

		xlsfile_text1 = datetime.datetime.now().strftime('%Y-%m-%d')

		#通过sheet_by_index()获取的sheet没有write()方法
		try:
			myWorkbook.save('database backup_'+ xlsfile_text1 + '.xls')
		except:
			print("提醒：\n保存数据到excel文件时，发现文件已打开！请关闭Excel文件！")
			input('文件已关闭了吗？已关闭，请点击Enter！')
			try:
				myWorkbook.save('database backup_'+ xlsfile_text1 + '.xls')
			except:
				print("文件未保存！")
		else:
			print('database backup_'+ xlsfile_text1 + '.xls'+",已保存更新！\n")
	conn.close()
dos_close = input('Press Enter to Exit')
