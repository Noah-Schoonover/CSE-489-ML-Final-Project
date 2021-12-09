#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import json
import keras
import numpy as np
import ConsolePlot as cp

model = keras.models.load_model('kerasModel.model')

async def hello(websocket, path):
    jsonData = await websocket.recv()

    data = json.loads(jsonData)

    npData = np.array(data).reshape((1, 784))
    npData2 = npData.reshape((28, 28))


    print("\n\n\n")    
    cp.printImage(npData2, 1, False)
    

    p = model.predict(npData)[0].tolist()
    print("p: ", p)
    print("prediction: ", p.index(max(p)))
    m = p.index(max(p))

    await websocket.send(json.dumps(m))

start_server = websockets.serve(hello, "127.0.0.1", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
