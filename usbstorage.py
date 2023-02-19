import os,subprocess

def handle(message:str):
    if message.startswith("load "):
        # return "image loaded" if load_mass_storage(message.removeprefix("load ")) else "image loading failed"
        return "image load"+str(load_mass_storage(message.removeprefix("load ")))
    elif message.startswith("unload"):
        unload_mass_storage()
        return "image unload: "+str(unload_mass_storage())
    else:
        return "unhandled "+message

def load_mass_storage(imagename:str):
    path=os.path.abspath("./usbimages/"+imagename)
    unloadConflictions()
    try:
        result=subprocess.run("sudo modprobe -v g_mass_storage file="+path,shell=True,stdout=subprocess.PIPE,encoding="UTF_8",timeout=5)
        # os.system("sudo modprobe g_mass_storage file="+path)
        return "ed: "+result.stdout.split("file=")[1].replace(os.path.abspath("./usbimages/"),"")
    except:
        return " failed"
def unload_mass_storage():
    try:
        result=subprocess.run("sudo modprobe -rv g_mass_storage",shell=True,stdout=subprocess.PIPE,encoding="UTF_8",timeout=5)
        # os.system("sudo modprobe -r g_mass_storage")
        return result.stdout
    except:
        return 0

def unloadConflictions():
    os.system("sudo modprobe -r g_ether")
    os.system("sudo modprobe -r g_serial")