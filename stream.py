import socket
from queue import Queue
import time
import struct

import picamera



class Output:
    def __init__(self, connection, q):
        self.conn = connection
        self.closed = False

    def write(self, buf):
        try:
            size = struct.pack(">I", len(buf))
            self.conn.send(size)
            self.conn.sendall(buf)

        except:
            self.closed = True

        return len(buf)


server = socket.socket()
server.bind(("", 8000))
server.listen(1)
cam = picamera.PiCamera()
q = Queue()


while True:
    print("[Server Ready]")
    conn, addr = server.accept()
    print(f"Connection established {addr}")
    out = Output(conn, q)
    cam.start_recording(out, format="mjpeg")

    while True:
        try:
            if out.closed:
                raise Exception()

            time.sleep(0.5)
        except:
            cam.stop_recording()
            #time.sleep()
            break

