import socket
import time
import struct

import picamera

from car import Car



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
            raise Exception()
            self.closed = True

        return len(buf)


stream_server = socket.socket()
stream_server.bind(("", 8000))
stream_server.listen(1)

control_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
control_sock.bind(("", 8080))

#cam = picamera.PiCamera(resolution=(640, 480))
cam = picamera.PiCamera(resolution=(320, 240))

while True:
    print("[Server Ready]")
    stream_conn, stream_addr = stream_server.accept()
    c = Car()
    print(f"Connection established {stream_addr}")
    out = Output(stream_conn)
    cam.start_recording(out, format="mjpeg")

    while True:
        try:
            if out.closed:
                break

            commands = control_sock.recvfrom(1024)[0].decode()
            commands = commands.split(",")

            for command in commands:
                name, value = command.split(":")

                if name == "SPEED":
                    speed = int(value)
                    c.speed(speed)
                if name == "STEER":
                    angle = int(value)
                    c.steer(angle)


        except:
            c.stop()
            c.terminate()
            break

    cam.stop_recording()

