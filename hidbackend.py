import os
import sys
import traceback
from ch9329lib import ch9329lib
import configHandler
__ch9329: ch9329lib.CH9329HID

def handle(message=""):
    global __ch9329
    try:
        execute=message.split(" ")
        if execute[0].__len__ and not (__ch9329 and __ch9329.getInfo()):
            init()
        if execute[0]=="pressKey":
            return pressKey(execute[1],int(execute[2]))
        elif execute[0]=="pressMouse":
            return pressMouse(execute[1],int(execute[2]))
        elif execute[0]=="mouseRelative":
            return mouseRelative(int(execute[1]),int(execute[2]),int(execute[3]))
        elif execute[0]=="mouseAbsolute":
            return mouseAbsolute(int(execute[1]),int(execute[2]),int(execute[3]))
        elif execute[0]=="mousePressButtons":
            return mousePressButtons(int(execute[1],base=2))
        elif execute[0]=="getInfo":
            return getInfo()
        if execute[0]=="getPressed":
            return getPressed()
        elif execute[0]=="releaseAll":
            return releaseAll()
        elif execute[0]=="disconnect":
            closeSerial()
            return "Closed Port"
        else:
            return "Error Can't handle this"
    except Exception as e:
        return "Exception: "+traceback.format_exc()
    
COMMON_BAUDRATES=[9600,115200,57600,38400,19200,4800,2400,1200]

def init():
    global __ch9329
    config=configHandler.config
    cfg_baudrate = int(config["hid"]["baudrate"])
    cfg_address = int(config["hid"]["ch9329_address"])
    cfg_serial_path = config["hid"]["serial_path"]
    if config["hid"]["hid_type"].startswith("ch9329"):
        if cfg_serial_path.startswith("tcp://"):
            __ch9329=ch9329lib.CH9329HID(True,cfg_serial_path.removeprefix("tcp://"),cfg_address,cfg_baudrate,False)
        else:
            __ch9329=ch9329lib.CH9329HID(False,cfg_serial_path,cfg_address,cfg_baudrate,False)
        if __ch9329.getInfo():
            print("Connected to CH9329 chip")
            return True
        elif not __ch9329.isOverTCP():
            return bool(try_fallback_baudrates(COMMON_BAUDRATES, cfg_baudrate))
        else:
            print(f"Can't connect to CH9329 chip with baudrate {cfg_baudrate}, check your configuration")
            return False
            
    else:
        raise UnknownHIDTypeException

def try_fallback_baudrates(fallback_bauds:list[int], cfg_baudrate:int):
    for baud in fallback_bauds:
        if try_baudrate(baud):
            if(cfg_baudrate not in COMMON_BAUDRATES):
                print(f"Configured baudrate {cfg_baudrate} is uncommon, not trying to change it automatically")
                return baud
            change_baudrate(cfg_baudrate)
            if try_baudrate(cfg_baudrate):
                return cfg_baudrate
            if try_baudrate(baud):
                return baud

def try_baudrate(baud:int):
    __ch9329.closeSerial()
    __ch9329.baud=baud
    __ch9329.initPort()
    info = __ch9329.getInfo()
    if(info):
        print(f"Connected to CH9329 chip with baudrate {baud}")
        return True
    return False

def change_baudrate(cfg_baudrate:int):
    cfg=__ch9329.getConfig()
    if(cfg):
        cfg.baudrate=cfg_baudrate
        print(f"Trying to set baudrate to {cfg_baudrate}")
        __ch9329.setConfig(cfg)
        __ch9329.reset()
        print(f"Set baudrate to {cfg_baudrate}")
        __ch9329.closeSerial()
    return True
        
def getPressed():
    pressedString=str()
    pressedTuple=__ch9329.getPressedKeyAll()
    for list in pressedTuple:
        for key in list:
            pressedString=pressedString+" "+key
    return "keyPressed "+pressedString
def pressKey(keyName,press=2):
    global __ch9329
    if press==2:
        __ch9329.pressByName(keyName,1)
        __ch9329.pressByName(keyName,0)
    else:
        __ch9329.pressByName(keyName,int(press))
    return getPressed()
def pressMouse(key,press=2):
    global __ch9329
    if press==2:
        __ch9329.mousePressClick(key,1)
        __ch9329.mousePressClick(key,0)
    else:
        __ch9329.mousePressClick(int(key),int(press))
    return "mousePressed "+str(__ch9329.getPressedMouse())
def mousePressButtons(buttons:int):
    __ch9329.mousePressButtons(buttons)
    return "mousePressed "+str(__ch9329.getPressedMouse())
def mouseRelative(x,y,wheel=0):
    global __ch9329
    return "mouseMove "+str(__ch9329.mouseRel(int(x),int(y),int(wheel)))
def mouseAbsolute(x,y,wheel=0):
    global __ch9329
    return "mouseMove "+str(__ch9329.mouseAbs(int(x),int(y),int(wheel)))
def getInfo():
    global __ch9329
    try:
        info=__ch9329.getInfo()
        if info:
            return "info "+f"locks={format(info[7],'03b')} usb={info[6]==1} ver={format(info[5],'02x')} "
        else:
            return "failed getinfo"
    except:
        return "failed getinfo"+traceback.format_exc()
def releaseAll():
    global __ch9329
    __ch9329.releaseAll()
    __ch9329.mouseReleaseAll()
    return getPressed()
def closeSerial():
    __ch9329.closeSerial()
    return "Info Disconnected"
class UnknownHIDTypeException(Exception):
    pass