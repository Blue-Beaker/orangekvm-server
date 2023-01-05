import configparser
import sys
import os
def __init__(file='orangekvm.ini'):
    global config
    config=readConfig(file)
    initConfig()
def readConfig(file='orangekvm.ini'):
    global config
    config = configparser.ConfigParser()
    config.read(file)
    return config
def initConfig():
    global config
    config=readConfig()
    if("server" not in config):
        config["server"]={}
    if("address" not in config["server"]):
        config["server"]["address"]="0.0.0.0"
    if("port" not in config["server"]):
        config["server"]["port"]='8000'
    if("path" not in config["server"]):
        config["server"]["path"]='web'
    if("websocket" not in config):
        config["websocket"]={}
    if("address" not in config["websocket"]):
        config["websocket"]["address"]="0.0.0.0"
    if("port" not in config["websocket"]):
        config["websocket"]["port"]='8001'
    if("stream" not in config):
        config["stream"]={}
    if("stream_url" not in config["stream"]):
        config["stream"]["stream_url"]="http://192.168.31.220:8080/stream"
    if("hid" not in config):
        config["hid"]={}
    if("hid_type" not in config["hid"]):
        config["hid"]["hid_type"]="ch9329_tty"
    if("hid_path" not in config["hid"]):
        config["hid"]["hid_path"]="/dev/ttyUSB0"
    if("ch9329_address" not in config["hid"]):
        config["hid"]["ch9329_address"]="0"
    if("baudrate" not in config["hid"]):
        config["hid"]["baudrate"]="9600"
    saveConfig()
def saveConfig():
    global config
    with open('orangekvm.ini', 'w+') as configfile:
        config.write(configfile)