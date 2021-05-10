import socket
import struct
import io

import pyglet
from pyglet.window import Window
from pyglet.clock import schedule_interval
from pyglet.image import ImageData
from PIL import Image



class Preview(Window):
    def __init__(self, address, width=720, height=480):
        super().__init__(width=width, height=height)
        self.sock = socket.socket()
        self.sock.connect(address)
        schedule_interval(self.update, 1e-7)

    def update(self, dt):
        received = 0
        img_buf = b""
        size_data = self.sock.recv(4)
        size = struct.unpack(">I", size_data)[0]

        while True:
            data = self.sock.recv(size-received)
            received += len(data)
            img_buf += data
            if size <= received:
                break

        img = Image.open(io.BytesIO(img_buf))
        #img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        img = ImageData(self.width, self.height, "RGB", img.tobytes("raw", "RGB"))

        img.blit(0, 0)


if __name__ == "__main__":
    p = Preview(("192.168.32.132", 8000), width=640, height=480)
    pyglet.app.run()
