import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('localhost',username=name,password=pw)
ssh.connect('localhost',username=name,password=pw,allow_agent=False,look_for_keys=False)