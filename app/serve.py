#!/usr/bin/env python3

try:
    import os
    from http.server import BaseHTTPRequestHandler, HTTPServer
        
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError
except Exception as e:
    print(f'[ERROR] {e}')

mes = os.environ.get('MESSAGE', 'Hackathon!')
m2m = os.environ.get('M2M', 'Hackathon!')
print(f'Message is {mes}')

PORT = int(os.environ.get('PORT', '8080'))
print(f'PORT is {PORT}')

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/ping':
            self.send_response(200)
            self.end_headers()
            return
        p=self.path.split('/')  
        
        if p[-1] == 'fault':
            self.send_response(503)
            self.end_headers()
            return

        if p[-2] == 'm2m':
            try:
                print(f'http://{m2m}/{p[-1]}')
                req = Request(f'http://{m2m}/{p[-1]}')
                res = urlopen(req)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(res.read())
                return 
            except Exception as e:
               self.send_response(500)
               self.wfile.write(bytes("Bad url", 'utf8'))
               return
           
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(mes, 'utf8'))

print('starting server...')
httpd = HTTPServer(('', PORT), Handler)
print('running server...')
httpd.serve_forever()
