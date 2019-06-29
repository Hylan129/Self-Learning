#!/usr/bin/python
# -*- coding: utf-8 -*-

import paramiko

# 创建SSH对象
ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname='10.10.12.180', port=22, username='user', password='',timeout=100)
#ssh.connect('localhost',username=name,password=pw,allow_agent=False,look_for_keys=False)
"""
# 执行命令
stdin, stdout, stderr = ssh.exec_command('ls')
# 获取命令结果
result = stdout.read()
print(result)

# 关闭连接
ssh.close()
"""
sftp = ssh.open_sftp()
sftp.get('C:\\AlarmCenter\\data\Debug.txt',r'C:\\Users\Administrator\\Desktop\\txt')
sftp.close()

"""
transport = paramiko.Transport(('10.10.12.20',22))
transport.connect(username='user',password='')
sftp = paramiko.SFTPClient.from_transport(transport)
# 将location.py 上传至服务器 /tmp/test.py
#sftp.put('/tmp/location.py', '/tmp/test.py')
# 将remove_path 下载到本地 local_path
sftp.get('C:\\AlarmCenter\\data\Debug.txt',r'C:\\Users\Administrator\\Desktop\\txt')
transport.close()
"""
