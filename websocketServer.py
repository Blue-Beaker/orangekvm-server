import asyncio
import websockets
import configHandler
import hidbackend
import atexit 
@atexit.register 
def clean(): 
    hidbackend.releaseAll()
    hidbackend.closeSerial()

async def handle(websocket, path):
    #fetch msg
    async for message in websocket:
        print("<- '{}'".format(message))
        message2=hidbackend.handle(message)
        await websocket.send(message2)
        print("-> '{}'".format(message2))
        message3=hidbackend.getInfo()
        await websocket.send(message3)
        print("-> '{}'".format(message3))

async def main():
    # start a websocket server
    async with websockets.serve(handle, configHandler.config["websocket"]["address"], configHandler.config["websocket"]["port"]):
        await asyncio.Future()  # run forever
def run():
    asyncio.run(main())