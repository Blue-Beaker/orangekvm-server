
import http
import http.server
import os
import sys

import configHandler
import http.client
import os
import sys

__KEYS=[{'`':['`',40,40],'1':['1',40,40],'2':['2',40,40],'3':['3',40,40],'4':['4',40,40],'5':['5',40,40],'6':['6',40,40],'7':['7',40,40],'8':['8',40,40],'9':['9',40,40],'0':['0',40,40],'-':['-',40,40],'=':['=',40,40],'back':['back',60,40]},
{'tab':['tab',50,40],'q':['q',40,40],'w':['w',40,40],'e':['e',40,40],'r':['r',40,40],'t':['t',40,40],'y':['y',40,40],'u':['u',40,40],'i':['i',40,40],'o':['o',40,40],'p':['p',40,40],'[':['[',40,40],']':[']',40,40],'\\':['\\',50,40]},
{'caps':['caps',60,40],'a':['a',40,40],'s':['s',40,40],'d':['d',40,40],'f':['f',40,40],'g':['g',40,40],'h':['h',40,40],'j':['j',40,40],'k':['k',40,40],'l':['l',40,40],';':[';',40,40],'\'':['\'',40,40],'enter':['enter',80,40]},
{'lshift':['shift',80,40],'z':['z',40,40],'x':['x',40,40],'c':['c',40,40],'v':['v',40,40],'b':['b',40,40],'n':['n',40,40],'m':['m',40,40],',':[',',40,40],'.':['.',40,40],'/':['/',40,40],'rshift':['shift',100,40]},
{'lctrl':['ctrl',60,40],'lwin':['win',40,40],'lalt':['alt',60,40],'space':['space',200,40],'menu':['menu',60,40],'ralt':['alt',60,40],'rwin':['win',40,40],'rctrl':['ctrl',60,40]}]

def getjs(file):
    path = sys.path[0]
    os.chdir(path)
    with open(file, 'r') as jsfile:
        return jsfile.read()
def virtKeyboard():
    keystr = ""
    for line in __KEYS:
        for key in line.keys():
            keystr=keystr+f"""<button type="button" onclick="pressKey('{key}',-1)" style="width:{line[key][1]}px;height:{line[key][2]}px;">{line[key][0]}</button>"""
        keystr=keystr+"<br>"
    return keystr
class ServerCore(http.server.BaseHTTPRequestHandler):
    timeout = 5
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","text/html")  #设置服务器响应头
        self.end_headers()
        page = f'''<!DOCTYPE HTML>
                <html>
                    <head>
                        <meta charset="utf-8"> 
                        <meta width=width-device initial-scale=1 user-scalable=0>
                        <title>OrangeKVM 0.1</title>
                    </head>
                    <script>
                    {getjs("orangekvm.js")}
                    linkws("ws://"+hostip+":{configHandler.config["websocket"]["port"]}/");
                    </script>
                <div id="content" style="background-color:#FFFFFF;width:1000px;float:top;">
                    <body>
                        <img src="{configHandler.config["stream"]["stream_url"]}" alt="{configHandler.config["stream"]["stream_url"]}" class="shrinkToFit" width="1000">
                    </body>
                </div>
                <div id="menu" style="background-color:#FFD700;width:1000px;float:top;">
                {virtKeyboard()}
                </div>
                </html>'''
        self.wfile.write(page.encode())

class Server:
    path=""
    def __init__(self,config):
        self.path = config['path']
        self.server = http.server.HTTPServer((config['address'],int(config["port"])),ServerCore)
    def serve_forever(self):
        self.server.serve_forever()
