from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os
from urllib.parse import urlparse, parse_qs
import cgi

POSTS_FILE = 'post.json'

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/posts':
            self.handle_get_posts()
        else:
            super().do_GET()

    def handle_get_posts(self):
        if os.path.exists(POSTS_FILE):
            with open(POSTS_FILE, 'r') as file:
                posts = json.load(file)
        else:
            posts = []

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(posts).encode())

    def do_POST(self):
        if self.path == '/api/posts':
            self.handle_post_request()
        else:
            super().do_POST()

    def handle_post_request(self):
        content_type = self.headers.get('Content-Type')
        if content_type.startswith('multipart/form-data'):
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
            
            title = form.getfirst('title')
            author = form.getfirst('author')
            content = form.getfirst('content')
            image_file = form['image'] if 'image' in form else None

            if title and author and (content or image_file):
                new_post = {
                    'title': title,
                    'author': author,
                    'content': content,
                }

                # Handle image file if uploaded
                if image_file:
                    image_path = os.path.join('uploads', image_file.filename)
                    with open(image_path, 'wb') as f:
                        f.write(image_file.file.read())
                    new_post['image'] = image_path

                if os.path.exists(POSTS_FILE):
                    with open(POSTS_FILE, 'r') as file:
                        posts = json.load(file)
                else:
                    posts = []

                posts.append(new_post)

                with open(POSTS_FILE, 'w') as file:
                    json.dump(posts, file)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Post created successfully!"}).encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Invalid post data."}).encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Unsupported Media Type."}).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
