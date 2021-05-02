import socket
import time
import struct

import picamera



class Output:
    def __init__(self, connection):
        self.conn = connection
        self.closed = False

    def write(self, buf):
        try:
            sent_len = 0
            size = len(buf)
            size_byte = struct.pack(">I", size)
            self.conn.send(size_byte)

            while sent_len != size:
                sent_len += self.conn.send(buf[sent_len:])

        except:
            print("Connection Reset")
            self.closed = True

        return len(buf)


server = socket.socket()
server.bind(("", 8000))
server.listen(1)
cam = picamera.PiCamera(resolution=(1280, 720), framerate=30)


while True:
    print("[Server Ready]")
    conn, addr = server.accept()
    print(f"Connection established {addr}")
    out = Output(conn)
    cam.start_recording(out, format="mjpeg")

    while True:
        try:
            if out.closed:
                break

            time.sleep(0.1)

        except:
            break

    cam.stop_recording()

