import socket
from queue import Queue

import picamera



class Output:
    def __init__(self, connection, q):
        self.conn = connection
        self.queue = q

    def write(self, buf):
        print(len(buf))


server = socket.socket()
cam = picamera.PiCamera()
q = Queue()


while True:
    conn, addr = server.accept()
    print(f"Connection established {addr}")
    out = Output(conn, q)
    cam.start_recording(out, format="mjpeg")

    while True:
        try:
            time.sleep(0.5)
        except Exception as e:
            print(e)
            cam.stop_recording()
            cam.close()
            break

