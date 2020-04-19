from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import uuid
import cgi
import json
import requests
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode


entries_dict = dict()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # API endpoints
        if self.path.startswith("/api"):

            if self.path.endswith("/all-entries"):
                self.send_response(200)
                self.send_header("content-type", "json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                response = json.dumps(entries_dict)
                self.wfile.write(response)

            if ("/entry") in self.path:
                self.send_response(200)
                self.send_header("content-type", "json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                # Gets path endpoint
                id = str(self.path).split("/")[-1]

                requested_post_data = entries_dict[id]
                response = json.dumps(requested_post_data)
                self.wfile.write(response)

            if self.path.endswith("weather"):
                self.send_response(200)
                self.send_header("content-type", "json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                # url = ""
                # # querystring = {}
                # headers = {}
                # response = requests.request("GET", url, headers=headers, params=querystring)
                # print(response.text)

                response = json.dumps()
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
                self.send_header("Content-Type", "json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                data = json.loads(body)

                new_ID = str(uuid.uuid4())
                date = data["date"]
                location = data["location"]
                narrative = data["narrative"]

                try:
                    connection = mysql.connector.connect(host='localhost',
                                                         database='devbros',
                                                         user='root',
                                                         password='!Five56five')
                    cursor = connection.cursor(prepared=True)
                    sql_insert_query = """INSERT INTO posts (id, date, location, narrative) VALUES (%s, %s, %s, %s)"""
                    data_input = (new_ID, date, location, narrative)
                    cursor.execute(sql_insert_query, data_input)
                    connection.commit()
                    print(cursor.rowcount, "Record inserted successfully into table")
                    cursor.close()

                except mysql.connector.Error as error:
                    print("Failed to insert record into table {}".format(error))

                finally:
                    if (connection.is_connected()):
                        connection.close()
                        print("MySQL connection is closed")


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

httpd = HTTPServer(('', 8100), SimpleHTTPRequestHandler)
httpd.serve_forever()
