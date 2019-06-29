import pymssql
import xlrd
import configparser

config = configparser.ConfigParser()
try:
	config.readfp(open(r'setting.ini'))
	host_set = config.get("sql_setting","host")
	user_set = config.get("sql_setting","user")
	password_set = config.get("sql_setting","password")
	database_set = config.get("sql_setting","database")
except:
	print("\n数据库连接setting配置文件异常，请检查setting.ini文件！\n")
else:
	conn=pymssql.connect(host=host_set,user=user_set,password=password_set,database=database_set,charset='utf8')
	cursor =conn.cursor()
	if not cursor:
		raise(NameError,"连接数据库失败,请检查setting设置参数！")
	else:
		print("\n\n %s 数据库连接成功!\n" % database_set)
			
		title_list = config.get("sql_setting","table_up").split('|')

		try:
			data = xlrd.open_workbook(r'database update.xls')
		except:
			print("待上传数据表database update.xls异常，缺失或者已打开！")
		else:
			if set(title_list) < set(data.sheet_names()):
				print("需要上传的数据表就绪！\n")
			else:
				print("请注意：table_up中的数据表名称，有部分未在database update数据表中找到！\n ")

			for list in range(len(title_list)):
				
				table_name = title_list[list]
				try:
					table_content = data.sheet_by_name(table_name)
				except:
					print(table_name+"数据表不存在！\n\n")
				else:
				
					#清空数据表
					sql_clear_0 = "Delete From "
					sql_clear = sql_clear_0 + table_name
					cursor.execute(sql_clear)
					conn.commit()
					print(" %s 旧数据表清空删除成功！"% table_name)
					
					table_title_list = table_content.row_values(0)
					table_type = []
					for number in range(table_content.ncols):
						type0 = type(table_content.row_values(1)[number])
						if type0 not in table_type:
							table_type.append(type0)
					print("新上传数据表数据类型共%d种,分别是："% len(table_type))
					print(table_type)
							
					#插入数据
						
					for row in range(1,table_content.nrows):
					
						sql_insert_1 = ",".join(table_title_list)
						
						table_row_content = table_content.row_values(row)
						sql_insert_plus = ''
						for number in range(table_content.ncols):
							
							if not isinstance(table_row_content[number] , str):
								sql_insert_plus = sql_insert_plus + str(table_row_content[number]) + ","
							else:
								sql_insert_plus = sql_insert_plus + "'" + table_row_content[number] +  "'"  + ","
						
						sql_insert_plus = sql_insert_plus.strip(',').replace('\u0000', '').replace('\x00', '')
						
						sql_insert = "INSERT INTO %s (%s) VALUES (%s)" % (table_name,sql_insert_1,sql_insert_plus)
						cursor.execute(sql_insert)
						conn.commit()
					print("数据表%s 共计插入%d行数据，已完成！\n\n" % (table_name,table_content.nrows-1))
	conn.close()
dos_close =input('\n Press Enter to exit...')
