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


stream_server = socket.socket()
stream_server.bind(("", 8000))
stream_server.listen(1)

control_server = socket.socket()
control_server.bind(("", 8080))
control_server.listen(1)

cam = picamera.PiCamera(resolution=(640, 480))


while True:
    print("[Server Ready]")
    control_conn, control_addr = control_server.accept()
    stream_conn, stream_addr = stream_server.accept()
    print(f"Connection established {stream_addr}")
    out = Output(stream_conn)
    cam.start_recording(out, format="mjpeg")

    while True:
        try:
            command = control_conn.recv(1024).decode()
            print(command)

            if out.closed:
                break

        except:
            break

    cam.stop_recording()

