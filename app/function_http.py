import socket
import os
import threading

import cv2
from PIL import Image


class OutputStream:
    def __init__(self):
        pass

    def write(self, buf):
        self.buf = buf

class HTTPHeaders:
    def __init__(self):
        self.header_dict = {}

    def parse(self, header_string) -> dict:
        headers = header_string.split("\r\n")[:-2]
        first_line = headers.pop(0)
        method, uri, version = first_line.split()
        self.header_dict["method"] = method
        self.header_dict["uri"] = uri
        self.header_dict["version"] = version

        for key_val in headers:
            key, val = key_val.split(": ")
            self.header_dict[key] = val
    
    def get(self):
        return self.header_dict

class HTTPServer:
    def __init__(self, server_sock):
        self.server_sock = server_sock
        self.conn = None
        self.cap = cv2.VideoCapture(0) ###############################################

    def wait_for_connection(self):
        self.conn, addr = self.server_sock.accept()
        print(addr)
        self.headers = HTTPHeaders()
        header_string = self.conn.recv(1024*4).decode()  # Header
        self.headers.parse(header_string)
        session_info = self.headers.get()

        if session_info["method"] == "GET":
            self.doGET(session_info)
        elif session_info["method"] == "POST":
            pass
        else:
            pass
    
    def start_header(self, response_code=200, msg="OK"):
        self.conn.send(f"HTTP/1.0 {str(response_code)} {str(msg)}\r\n".encode())

    def add_header(self, key, val):
        self.conn.send(f"{str(key)}: {str(val)}\r\n".encode())

    def end_header(self):
        self.conn.send(b"\r\n")
    
    def doGET(self, headers):
        path = headers["uri"][1:]
        
        if path != "stream.mjpg":
            if path == "":
                path = "index.html"
            
            if not os.path.exists(path):
                self.start_header(404, "NOTFOUND")
                self.end_header()
                self.conn.close()
                return
            
            print(path)
            with open(path, "rb") as f:
                filedata = f.read()

            self.start_header()
            self.add_header("Content-Length", len(filedata))
            #self.add_header("Content-Type", )
            self.end_header()
            self.conn.sendall(filedata)
            self.conn.close()
        else:  # path = "stream.mjpg"
            self.start_header()
            self.add_header("Content-Type", "multipart/x-mixed-replace; boundary=FRAME")
            self.end_header()

            while True:
                ret, img = self.cap.read()
                if not ret:
                    continue

                image = Image.fromarray(img[:, :, ::-1]).tobytes("jpeg", "RGB")
                #image = open("test.jpg", "rb").read()

                self.conn.send(b"--FRAME\r\n")
                self.add_header('Age', 0)
                self.add_header('Cache-Control', 'no-cache, private')
                self.add_header('Pragma', 'no-cache')
                self.add_header("Content-Type", "image/jpeg")
                self.add_header("Content-Length", len(image))
                self.end_header()

                self.conn.sendall(image)
                self.conn.send(b"\r\n")

    def client_loop(self):
        while True:
            self.wait_for_connection()

    def client_loop_in_thread(self):
        thread = threading.Thread(target=self.client_loop)
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    sock = socket.socket()
    sock.bind(("", 8000))
    sock.listen(1)
    server = HTTPServer(sock)
    server.client_loop()
