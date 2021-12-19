#! /home/noah/digit-ml/venv/bin/python3

# WS server example

import asyncio
import websockets
import json
import keras
import numpy as np
import ConsolePlot as cp

print("loading model...")

model = keras.models.load_model('kerasModel.model')

print("done.")
print("Waiting for requests...")

async def hello(websocket, path):
    jsonData = await websocket.recv()
    
    print("\n\n\n") 
    
    #print(f"data: {jsonData}")
    print("jsonData length: ", len(jsonData))

    data = json.loads(jsonData)
    print("data length: ", len(data))

    npData = np.array(data).reshape((1, 784))
    print("npData.shape: ", npData.shape)

    npData2 = np.array(data).reshape((28, 28))
    print("shape debug: ", npData2.shape)
    cp.printImage(npData2, 1, False)
    

    p = model.predict(npData)[0].tolist()
    print("p: ", p)
    print("max p: ", max(p))
    print("index: ", p.index(max(p)))
    m = p.index(max(p))

    await websocket.send(json.dumps(m))

start_server = websockets.serve(hello, "", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
