#! /bin/python3
import configparser
import sys
import os
import configHandler
import httpServer
import websocketServer
import threading
import hidbackend
import scripts
if __name__ == '__main__':
    path = sys.path[0]
    os.chdir(path)
    scripts.onStart()
    configHandler.__init__()
    wsthread=threading.Thread(target = websocketServer.run)
    wsthread.daemon=True
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
    
