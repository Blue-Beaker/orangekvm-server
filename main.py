import configparser
import sys
import os
import configHandler
import httpServer
import websocketServer
import threading
import hidbackend

if __name__ == '__main__':
    path = sys.path[0]
    os.chdir(path)
    print(path)
    configHandler.__init__()
    wsthread=threading.Thread(target = websocketServer.run)
    wsthread.setDaemon(True)
    print("Starting Websocket server")
    wsthread.start()
    print("Started Websocket server")
    # websocketServer.run()
    server = httpServer.Server(configHandler.config["server"])
    httpthread=threading.Thread(target = server.serve_forever)
    print("Starting HTTP server")
    httpthread.start()
    print("Started HTTP server")
    hidbackend.init()
    