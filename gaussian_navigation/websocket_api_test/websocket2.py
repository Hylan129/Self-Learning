from websocket import create_connection
ws = create_connection("ws://10.7.5.88:8089/gs-robot/notice/status")
print("Sending 'Hello, World'...")
ws.send("Hello, World")
print("Sent")
print("Receiving...")
result =  ws.recv()
print("Received '%s'" % result)
ws.close()