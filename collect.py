import socket
import struct
import io
import os

import pyglet
from pyglet.window import Window
from pyglet.clock import schedule_interval
from pyglet.image import ImageData
from pyglet.window import key
from PIL import Image
import cv2
import numpy as np

from raspi_ip import IP


W = 320
H = 240

def gen_name(dir):
    i = 0
    
    while True:
        if not os.path.exists(dir + "/" + f"img-{i}.jpg"):
            break

        i += 1

    return dir + "/" + f"img-{i}.jpg"

"""
def image_preprocess(img):
    array = np.array(img)
    sobel_x = cv2.Sobel(array, cv2.CV_32F, 1, 0)
    sobel_y = cv2.Sobel(array, cv2.CV_32F, 0, 1)
    sobel = (sobel_x + sobel_y) // 2
    sobel -= sobel.min()
    sobel = sobel / sobel.max()
    sobel *= 255
    sobel = sobel.astype(np.uint8)
    sobel = Image.fromarray(sobel).convert("RGB")
    return sobel
"""
def image_preprocess(img):
    img = img.convert("L")
    array = np.array(img, dtype=np.int32)
    res = np.zeros_like(array)

    res[array > np.average(array) + 30] = 255

    img = Image.fromarray(res.astype(np.uint8))
    return img.convert("RGB")


class Preview(Window):
    def __init__(self, ip, width=720, height=480):
        super().__init__(width=width, height=height)
        self.control_sock = socket.socket()
        self.stream_sock = socket.socket()
        self.stream_sock.connect((ip, 8000))
        self.control_sock.connect((ip, 8080))
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
        img = img.transpose(Image.FLIP_LEFT_RIGHT) # To show
        preprocessed = image_preprocess(img) # To show

        self.img = img.transpose(Image.FLIP_TOP_BOTTOM) # To save
        self.preprocessed = preprocessed.transpose(Image.FLIP_TOP_BOTTOM) # To save

        img = preprocessed

        img = ImageData(self.width, self.height, "RGB", img.tobytes("raw", "RGB"))
        img.blit(0, 0)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.control_sock.send(b"SPEED:100")
        elif symbol == key.DOWN:
            self.control_sock.send(b"SPEED:-100")
        elif symbol == key.LEFT:
            self.control_sock.send(b"STEER:-20")
        elif symbol == key.RIGHT:
            self.control_sock.send(b"STEER:20")
        elif symbol == key.ENTER:
            name = gen_name("train_data")
            self.img.save(name)
            print(name)

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
    print(IP)
    p = Preview(IP, width=W, height=H)
    pyglet.app.run()
