import os

def handle(message:str):
    if message.startswith("load "):
        return "image loaded" if load_mass_storage(message.removeprefix("load ")) else "image loading failed"
    elif message.startswith("unload"):
        unload_mass_storage()
        return "image unloaded"
    else:
        return "unhandled "+message

def load_mass_storage(imagename:str):
    path=os.path.abspath("./usbimages/"+imagename)
    unloadConflictions()
    return os.system("sudo modprobe g_mass_storage file="+path)
def unload_mass_storage():
    os.system("sudo modprobe -r g_mass_storage")

def unloadConflictions():
    os.system("sudo modprobe -r g_ether")
    os.system("sudo modprobe -r g_serial")