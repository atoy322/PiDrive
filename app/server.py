import socket
import queue

import picamera



def parse_header(header_string):
    result_dict = dict()
    lines = header_string.split("\r\n")[:-2]
    line1 = lines.pop(0)
    method, uri, version = line1.split(" ")
    result_dict["method"] = method
    result_dict["uri"] = uri
    result_dict["version"] = version

    for line in lines:
        key, val = line.split(": ")
        result_dict[key] = val
    
    return result_dict



##### main #####
sock = socket.socket()
sock.bind(("", 8000))
sock.listen(1)

class RadioControlServer:
    def __init__(self, sock):
        self.sock = sock
        self.conn = None
        self.frame_queue = queue.Queue()
        self.camera = picamera.PiCamera(width=640, height=480)
        self.camera.start_recording(self, format="mjpeg")

    def write(self, data):
        if self.frame:
            print("[frame sending]")
            self.conn.sendall(data)

    def accept(self):
        self.conn, addr = sock.accept()
        print(addr) ###
        header = self.conn.recv(1024).decode()  # Request Header (1 kB)
        print(parse_header(header)) ###
