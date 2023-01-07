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
    printMsg=0
    async for message in websocket:
        if printMsg:
            print("<- '{}'".format(message))
        message2=hidbackend.handle(message)
        if printMsg:
            print("-> '{}'".format(message2))
        message3=hidbackend.getInfo()
        for socket in websocket.ws_server.websockets:
            await socket.send(message2)
            await socket.send(message3)


async def main():
    # start a websocket server
    async with websockets.serve(handle, configHandler.config["server"]["address"], configHandler.config["server"]["wsport"]):
        await asyncio.Future()  # run forever
def run():
    asyncio.run(main())