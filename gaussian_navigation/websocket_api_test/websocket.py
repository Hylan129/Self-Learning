#!/usr/bin/env python

import asyncio
import websockets
import json

async def test_ws_quote():
    async with websockets.connect('ws://10.7.5.88:8089/gs-robot/notice/device_status') as websocket:
        #req = {"protocol":"history_req",'code':'XAGODS','type':'MINUTE','start_pos':'0','pos_num':'10'}
        #await websocket.onmessage(json.dumps(req))
   
        while True:
            quote = await websocket.recv()
            print(quote)

asyncio.get_event_loop().run_until_complete(test_ws_quote())