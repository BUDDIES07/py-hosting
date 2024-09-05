from http.server import SimpleHTTPRequestHandler, HTTPServer
import json

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/posts':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            with open('post.json', 'r') as file:
                self.wfile.write(file.read().encode('utf-8'))
        else:
            super().do_GET()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
