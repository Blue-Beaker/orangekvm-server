
import datetime
import http
import http.server
from http import HTTPStatus
import os
import sys
import urllib

import configHandler
import http.client

__KEYS=[
{'esc':['esc',1,1],'f1':['F1',1,1],'f2':['F2',1,1],'f3':['F3',1,1],'f4':['F4',1,1],'f5':['F5',1,1],'f6':['F6',1,1],'f7':['F7',1,1],'f8':['F8',1,1],'f9':['F9',1,1],'f10':['F10',1,1],'f11':['F11',1,1],'f12':['F12',1,1],'printscreen':['Print',1,1]},
{'`':['`',1,1],'1':['1',1,1],'2':['2',1,1],'3':['3',1,1],'4':['4',1,1],'5':['5',1,1],'6':['6',1,1],'7':['7',1,1],'8':['8',1,1],'9':['9',1,1],'0':['0',1,1],'-':['-',1,1],'=':['=',1,1],'backspace':['back',1,1]},
{'tab':['tab',1.25,1],'q':['q',1,1],'w':['w',1,1],'e':['e',1,1],'r':['r',1,1],'t':['t',1,1],'y':['y',1,1],'u':['u',1,1],'i':['i',1,1],'o':['o',1,1],'p':['p',1,1],'[':['[',1,1],']':[']',1,1],'\\\\':['\\',0.75,1]},
{'caps':['caps',1.5,1],'a':['a',1,1],'s':['s',1,1],'d':['d',1,1],'f':['f',1,1],'g':['g',1,1],'h':['h',1,1],'j':['j',1,1],'k':['k',1,1],'l':['l',1,1],';':[';',1,1],'\'':['\'',1,1],'enter':['enter',1.5,1]},
{'lshift':['shift',2,1],'z':['z',1,1],'x':['x',1,1],'c':['c',1,1],'v':['v',1,1],'b':['b',1,1],'n':['n',1,1],'m':['m',1,1],',':[',',1,1],'.':['.',1,1],'/':['/',1,1],'rshift':['shift',2,1]},
{'lctrl':['ctrl',1.5,1],'lsuper':['win',1,1],'lalt':['alt',1.5,1],'space':['space',5,1],'app':['menu',1.25,1],'ralt':['alt',1.5,1],'rsuper':['win',1,1],'rctrl':['ctrl',1.25,1]}]

def getjs(file):
    path = sys.path[0]
    os.chdir(path)
    with open(file, 'r') as jsfile:
        return jsfile.read()
def virtKeyboard():
    keystr = ""
    for line in __KEYS:
        for key in line.keys():
            keystr=keystr+f"""<button id="keyboard_{key}" type="button" onclick="pressKey('{key}',-1)" style="width:{line[key][1]/14*100}%;height:{line[key][2]*40}px;">{line[key][0]}</button>"""
        keystr=keystr+"<br>"
    return keystr
class ServerCore(http.server.BaseHTTPRequestHandler):
    timeout = 5
    def do_GET(self):
        page = f'''<!DOCTYPE HTML>
                    <html>
                        <head>
                            <meta charset="utf-8"> 
                            <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0"/>
                            <title>OrangeKVM 0.1</title>
                        </head>
                        <script>
                        {getjs("orangekvm.js")}
                        function reconnect(){{
                            linkws("ws://"+hostip+":{configHandler.config["websocket"]["port"]}/");
                        }}
                        reconnect()
                        </script>
                        <noscript>Your browser doesn't allow javascript. Please use a browser with javascript and websocket enabled.</noscript>
                        <body style="background-color:#FFFFFF;width:100%;height:70%;float:top;">
                            <img src="{configHandler.config["stream"]["stream_url"]}" alt="{configHandler.config["stream"]["stream_url"]}" class="shrinkToFit" width=95%>
                        </body>
                        <button id="releaseAll" text="Release All" onclick="releaseAll()">Release All</button>
                        <div id="keyboard" style="background-color:#FF8F00;width:100%;height:300px;float:top">
                            <div id="keyboard1" style="width:100%;float:left">
                                {virtKeyboard()}
                            </div>
                            <div id="keyboard2" style="width:120px;float:left">
                                {""}
                            </div>
                            <div id="keyboard3" style="width:160px;float:left">
                                {""}
                            </div>
                        </div>
                    </html>'''
        self.send_response(200)
        self.send_header("Content-type","text/html")  #设置服务器响应头
        self.end_headers()
        self.wfile.write(page.encode())

class ServerCore2(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Serve a GET request."""
        f,ctype = self.send_head()
        if f:
            try:
                if ctype=="text/html":
                    __DICT={
                        "wsport":configHandler.config["websocket"]["port"],
                        "streamurl":configHandler.config["stream"]["stream_url"],
                        "keyboard1":virtKeyboard(),
                        "keyboard2":"",
                        "keyboard3":""
                    }
                    pagestr=f.read().decode()
                    self.wfile.write(pagestr.format(**__DICT).encode())
                else:
                    self.copyfile(f, self.wfile)
            finally:
                f.close()
    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            parts = urllib.parse.urlsplit(self.path)
            if not parts.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                new_parts = (parts[0], parts[1], parts[2] + '/',
                             parts[3], parts[4])
                new_url = urllib.parse.urlunsplit(new_parts)
                self.send_header("Location", new_url)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        # check for trailing "/" which should return 404. See Issue17324
        # The test for this was added in test_httpserver.py
        # However, some OS platforms accept a trailingSlash as a filename
        # See discussion on python-dev and Issue34711 regarding
        # parseing and rejection of filenames with a trailing slash
        if path.endswith("/"):
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None
        try:
            fs = os.fstat(f.fileno())
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", ctype)
            # self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified",
                self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f,ctype
        except:
            f.close()
            raise


class Server:
    path=""
    def __init__(self,config):
        self.path = config['path']
        # self.server = http.server.HTTPServer((config['address'],int(config["port"])),ServerCore)
        self.server = http.server.HTTPServer((config['address'],int(config["port"])),ServerCore2)
    def serve_forever(self):
        self.server.serve_forever()
