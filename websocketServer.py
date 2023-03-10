import asyncio
import traceback
import websockets
from websockets.server import WebSocketServerProtocol
import configHandler
import hidbackend,usbstorage
import atexit 
printMsg:int
@atexit.register 
def clean(): 
    try:
        hidbackend.releaseAll()
        hidbackend.closeSerial()
    except:
        pass

async def handle(websocket: WebSocketServerProtocol, path):
    try:
        async for message in websocket:
            message=str(message)
            if printMsg:
                print("<- '{}'".format(message))
            if str(message).startswith("image"):
                message2=usbstorage.handle(message.removeprefix("image"))
            else:
                message2=hidbackend.handle(str(message))
            if printMsg:
                print("-> '{}'".format(message2))
            for socket in websocket.ws_server.websockets:
                await socket.send(message2)
    except websockets.exceptions.ConnectionClosed:
        if websocket.ws_server.websockets.__len__()==0:
            try:
                hidbackend.closeSerial()
            except:
                traceback.print_exc()


async def main():
    # start a websocket server
    async with websockets.serve(handle, configHandler.config["server"]["address"], int(configHandler.config["server"]["wsport"])):
        await asyncio.Future()  # run forever
def run():
    global printMsg
    printMsg=int(configHandler.config["server"]["wsprintmessage"])
    asyncio.run(main())