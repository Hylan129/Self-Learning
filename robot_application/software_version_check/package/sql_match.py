import pymssql

def getDllinformation_inSQL():
    server="10.7.5.105"
    user="sa"
    password="qxznqipai!"

    conn=pymssql.connect(host=server,user=user,password=password,database='DatabaseSQLRobot',charset='utf8')
    cursor=conn.cursor()
    cursor.execute("select equip_no,equip_nm,communication_drv,local_addr from Equip")
    rows = cursor.fetchall()
    cursor.close()

    return rows
