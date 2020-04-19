from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import uuid
import cgi
import json
import requests
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path.startswith("/api"):

            if self.path.endswith("/all-entries"):
                self.send_response(200)
                self.send_header("content-type", "json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                try:
                    connection = mysql.connector.connect(host='localhost',
                                                         database='devbros',
                                                         user='root',
                                                         password='!Five56five')
                    cursor = connection.cursor(prepared=True)
                    sql_insert_query = """SELECT * FROM posts;"""
                    cursor.execute(sql_insert_query)
                    response = cursor.fetchall()
                    connection.commit()
                    cursor.close()

                except mysql.connector.Error as error:
                    print("Failed to access records".format(error))

                finally:
                    if (connection.is_connected()):
                        connection.close()
                        print("MySQL connection is closed")

                self.wfile.write(json.dumps(response).encode())

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

    def do_POST(self):

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

    def do_DELETE(self):

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
