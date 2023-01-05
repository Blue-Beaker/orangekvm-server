import configparser
import sys
import os
import configHandler
import httpServer
import websocketServer
import threading

if __name__ == '__main__':
    path = sys.path[0]
    os.chdir(path)
    print(path)
    configHandler.__init__()
    wsthread=threading.Thread(target = websocketServer.run)
    wsthread.setDaemon(True)
    print("Starting Websocket server")
    wsthread.start()
    # websocketServer.run()
    server = httpServer.Server(configHandler.config["server"])
    print("Starting HTTP server")
    server.serve_forever()
    
    