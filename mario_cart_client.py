import socket
import struct
import io

import pyglet
from pyglet.window import Window
from pyglet.clock import schedule_interval
from pyglet.image import ImageData
from pyglet.window import key
from PIL import Image



RASPI_IP = "192.168.183.132"

class Preview(Window):
    def __init__(self, ip, width=720, height=480):
        super().__init__(width=width, height=height)
        self.control_sock = socket.socket()
        self.stream_sock = socket.socket()
        self.control_sock.connect((ip, 8080))
        self.stream_sock.connect((ip, 8000))
        schedule_interval(self.update, 1e-3)

    def update(self, dt):
        received = 0
        img_buf = b""
        size_data = self.stream_sock.recv(4)
        size = struct.unpack(">I", size_data)[0]

        while True:
            data = self.stream_sock.recv(size-received)
            received += len(data)
            img_buf += data
            if size <= received:
                break

        img = Image.open(io.BytesIO(img_buf))
        #img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img = img.transpose(Image.FLIP_LEFT_RIGHT).resize((self.width, self.height))
        img = ImageData(self.width, self.height, "RGB", img.tobytes("raw", "RGB"))

        img.blit(0, 0)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.control_sock.send(b"SPEED:50")
        elif symbol == key.DOWN:
            self.control_sock.send(b"SPEED:-50")
        elif symbol == key.LEFT:
            self.control_sock.send(b"STEER:-30")
        elif symbol == key.RIGHT:
            self.control_sock.send(b"STEER:30")

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.control_sock.send(b"SPEED:0")
        elif symbol == key.DOWN:
            self.control_sock.send(b"SPEED:0")
        elif symbol == key.LEFT:
            self.control_sock.send(b"STEER:0")
        elif symbol == key.RIGHT:
            self.control_sock.send(b"STEER:0")


if __name__ == "__main__":
    p = Preview(RASPI_IP, width=320, height=240)
    pyglet.app.run()
