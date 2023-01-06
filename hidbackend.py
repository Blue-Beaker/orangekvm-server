from ch9329lib import ch9329lib
import configHandler
__ch9329 = None

def handle(message=""):
    global __ch9329
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
    elif execute[0]=="getInfo":
        return getInfo()
    if execute[0]=="getPressed":
        return getPressed()
    elif execute[0]=="releaseAll":
        return releaseAll()
    elif execute[0]=="disconnect":
        closeSerial()
    else:
        return "Error Can't handle this"
def init():
    global __ch9329
    config=configHandler.readConfig()
    if config["hid"]["hid_type"].startswith("ch9329_"):
        __ch9329=ch9329lib.CH9329HID(config["hid"]["hid_type"]==("ch9329_tcp"),config["hid"]["hid_path"],int(config["hid"]["ch9329_address"]),config["hid"]["baudrate"],False)
    else:
        raise UnknownHIDTypeException
def getPressed():
    pressedString=""
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
        __ch9329.pressByName(keyName,press)
    return getPressed()
def pressMouse(key,press=2):
    global __ch9329
    if press==2:
        __ch9329.mousePressClick(key,1)
        __ch9329.mousePressClick(key,0)
    else:
        __ch9329.mousePressClick(key,press)
    return "mousePressed "+str(__ch9329.getPressedMouse())
def mouseRelative(x,y,wheel=0):
    global __ch9329
    return "mouseMove "+str(__ch9329.mouseRel(x,y,wheel))
def mouseAbsolute(x,y,wheel=0):
    global __ch9329
    return "mouseMove "+str(__ch9329.mouseAbs(x,y,wheel))
def getInfo():
    global __ch9329
    return "info "+str(__ch9329.getInfo())
def releaseAll():
    global __ch9329
    if __ch9329:
        __ch9329.releaseAll()
        return getPressed()
def closeSerial():
    global __ch9329
    if __ch9329:
        __ch9329.closeSerial()
        return "Info Disconnected"
class UnknownHIDTypeException(Exception):
    pass