from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import uuid
import cgi
import json

entries_dict = {"1": "First post", "2": "Second Post"}

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # API endpoints
        if self.path.startswith("/api"):

            if self.path.endswith("/all-entries"):
                self.send_response(200)
                self.send_header("content-type", "json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                response = json.dumps(entries_dict).encode()
                self.wfile.write(response)

            if ("/entry") in self.path:
                self.send_response(200)
                self.send_header("content-type", "json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                # Gets path endpoint
                id = str(self.path).split("/")[-1]

                requested_post_data = entries_dict[id]
                response = json.dumps(requested_post_data).encode()
                self.wfile.write(response)

        # HTML router
        else:
            if self.path.endswith("/entries"):
                self.send_response(200)
                self.send_header("content-type", "text/html")
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Entry List</h1>"
                output += "<h3><a href='/entries/new'>Add New Entry</a></h3>"
                for entry in entries_list:
                    output += entry
                    output += "</br>"
                output += "</body></html>"
                self.wfile.write(output.encode())

            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header("content-type", "text/html")
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Add New Entry</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/entries/new'>"
                output += "<input name='entry' type='text' placeholder='Add new entry'>"
                output += "<input type='submit' value='Add'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output.encode())

    def do_POST(self):
        # API endpoints
        if self.path.startswith("/api"):
            # Endpoint for adding single entry
            if self.path.endswith("/new-entry"):
                self.send_response(200)
                self.send_header("content-type", "json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                data = body.decode()
                new_ID = str(uuid.uuid4())
                entries_dict[new_ID] = data

                # Returns ID for new post
                response = json.dumps(new_ID).encode()
                self.wfile.write(response)
        # HTML router
        else:
            if self.path.endswith("/new"):
                ctype, pdict = cgi.parse_header(self.headers.get("content-type"))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                content_len = int(self.headers.get('Content-length'))
                pdict['CONTENT-LENGTH'] = content_len
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_entry = fields.get("entry")
                    entries_list.append(new_entry[0])

                    self.send_response(301)
                    self.send_header("content-type", "text/html")
                    self.send_header("Location", "/entries")
                    self.end_headers()

    def do_DELETE(self):
        # API endpoints
        if self.path.startswith("/api"):
            if ("/entry") in self.path:
                self.send_response(200)
                self.send_header("content-type", "json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                id = str(self.path).split("/")[-1]
                del(entries_dict[id])

                response = json.dumps(None).encode()
                self.wfile.write(response)

            if self.path.endswith("/all-entries"):
                self.send_response(200)
                self.send_header("content-type", "json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                entries_dict.clear()

                response = json.dumps(None).encode()
                self.wfile.write(response)

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
