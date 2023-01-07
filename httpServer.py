import http
import http.server
from http import HTTPStatus
import os
import sys
import urllib
import configHandler
import http.client
import constants

def getjs(file):
    path = sys.path[0]
    os.chdir(path)
    with open(file, 'r') as jsfile:
        return jsfile.read()
def virtKeyboard(keymap: list[dict[str,list[str,float,float]]],columns):
    keystr = ""
    for y in range(keymap.__len__()):
        x=0
        line=keymap[y]
        for key in line.keys():
            addBackslash=key=="'" or key=="\\"
            backslash="\\"
            x=x+line[key][3] if line[key].__len__()>=4 else x
            keystr=keystr+f"""<button class='key' id="keyboard_{key}" type="button" onclick="pressKey('{key if not addBackslash else backslash+key}',-1)" style="
                width:{line[key][1]/columns*100}%; height:{line[key][2]*40}px;
                position:absolute; left:{x/columns*100}%; top:{y*40}px;"> {line[key][0]} </button>"""
            x=x+line[key][1]
    return keystr

class ServerCore2(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Serve a GET request."""
        try:
            f,ctype = self.send_head()
            if f:
                try:
                    if ctype=="text/html":
                        __DICT={
                            "wsport":configHandler.config["websocket"]["port"],
                            "streamurl":configHandler.config["stream"]["stream_url"],
                            "keyboard1":virtKeyboard(constants.KEYBOARD.KEYS1,14),
                            "keyboard2":virtKeyboard(constants.KEYBOARD.KEYS2,3),
                            "keyboard3":virtKeyboard(constants.KEYBOARD.KEYS3,4)
                        }
                        pagestr=f.read().decode()
                        self.wfile.write(pagestr.format(**__DICT).encode())
                    else:
                        self.copyfile(f, self.wfile)
                finally:
                    f.close()
        except:
            pass
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
    def __init__(self,config:configHandler.configparser.ConfigParser):
        self.server = http.server.HTTPServer((config['address'],int(config["port"])),ServerCore2)
    def serve_forever(self):
        self.server.serve_forever()
