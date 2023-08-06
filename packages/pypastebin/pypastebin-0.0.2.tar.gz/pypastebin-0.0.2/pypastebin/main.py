from http.server import BaseHTTPRequestHandler, HTTPServer
from pypastebin.pages.api import *
from pypastebin.pages.index import *
from pypastebin.pages.view import *
from pypastebin.database import *
import time, os, urllib.parse
from urllib.parse import urlparse, parse_qs

class request_data:
    def __init__(self):
        self.headers = None
        self.path = None
        self.database = None
        self.httpd = None
        self.POST = None
        self.post_data = None

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        # read post request values
        post_data = ""
        if "Content-Length" in self.headers:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8", errors='ignore')
        self.send_response(200)
        r = request_data()
        r.path = self.path
        r.headers = self.headers
        r.database = database
        r.httpd = self
        r.post_data = post_data
        r.POST = self.read_values(post_data)
        # get response from path
        resp = ""
        if self.path == "/api":
            self.send_header("Content-type", "text/html ; charset=utf-8")
            resp = add_paste(r)
        elif self.path == "/":
            self.send_header("Content-type", "text/html ; charset=utf-8")
            resp = index_html(r);
        else:
            self.send_header("Content-type", "text/plain ; charset=utf-8")
            resp = view_paste(r);
            
        # write response
        self.end_headers()
        self.wfile.write(str(resp).encode("utf-8", errors='ignore'))

    def do_POST(self):
        return self.do_GET()


    def read_values(self, data):
        ret = {}
        qs = parse_qs(data)
        for var in qs.keys():
            ret[var] = qs[var][0]
        return ret


database = database()

def start_server(port):

    webServer = HTTPServer(("0.0.0.0", port), MyServer)
    print("Server started http://0.0.0.0:%s" % (port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

if __name__ == "__main__":
    start_server(settings.port)

