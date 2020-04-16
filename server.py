from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import uuid

content = "gone fishin"

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        globals_list = globals()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(globals_list["content"], "utf-8"))

    def do_POST(self):
        global content
        content_length = int(self.headers['Content-Length'])
        request = self.rfile.read(content_length)
        id = bytes(str(uuid.uuid4()), "utf-8")
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'Your entry ID is: ')
        response.write(id)
        content = str(request)
        self.wfile.write(response.getvalue())




httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
