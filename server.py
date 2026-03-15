#!/usr/bin/env python3
import json
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer

INDEX = os.path.join(os.path.dirname(__file__), 'index.html')

class Handler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        if self.path == '/save':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                html = data.get('html', '')
                with open(INDEX, 'w', encoding='utf-8') as f:
                    f.write(html)
                self.send_response(200)
                self._cors()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
            except Exception as e:
                self.send_response(500)
                self._cors()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': False, 'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, format, *args):
        print(f"  {self.address_string()} — {format % args}")

if __name__ == '__main__':
    port = 3000
    server = HTTPServer(('', port), Handler)
    print(f"✓ Chatfor editor server running at http://localhost:{port}")
    print(f"  Editing: {INDEX}")
    print(f"  Press Ctrl+C to stop\n")
    server.serve_forever()
