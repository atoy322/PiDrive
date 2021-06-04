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
from chainer import Chain
from chainer.links import Linear, Convolution2D
from chainer.functions import relu, softmax_cross_entropy
from chainer.variable import Variable

from raspi_ip import IP


conv = Convolution2D(3, 1, 3)
edge_filter = np.array([[
    [[ 0, -1,  0],
     [-1,  1,  -1],
     [ 0, -1,  0]],

    [[ 0, -1,  0],
     [-1,  1, -1],
     [ 0, -1,  0]],

    [[ 0, -1,  0],
     [-1,  1, -1],
     [ 0, -1,  0]]
]], dtype=np.float32)
conv.W = Variable(edge_filter)

def gen_name(dir):
    i = 0
    
    while True:
        if not os.path.exists(dir + "/" + f"img-{i}.jpg"):
            break

        i += 1

    return dir + "/" + f"img-{i}.jpg"


def detect_line(img):
    array = np.array(img)
    sobel_x = cv2.Sobel(array, cv2.CV_32F, 1, 0)
    sobel_y = cv2.Sobel(array, cv2.CV_32F, 0, 1)
    sobel = (sobel_x + sobel_y) // 2
    sobel -= sobel.min()
    sobel = sobel / sobel.max()
    sobel *= 255
    sobel = sobel.astype(np.uint8)
    sobel = Image.fromarray(sobel).convert("L").convert("RGB")
    return sobel

def detect_line_conv(img):
    w, h = img.size
    array = np.array(img, dtype=np.float32)
    array = array.transpose(2, 0, 1).reshape(1, 3, h, w)
    array = conv(array)[0][0].array.transpose(1, 0)
    array -= array.min()
    array = array / array.max()
    array *= 255
    img = Image.fromarray(array.astype(np.uint8)).convert("RGB")
    return img


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
        self.img = img.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)
        img = img.transpose(Image.FLIP_LEFT_RIGHT).resize((self.width, self.height))
        img = detect_line(img)
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
            sobel = detect_line(self.img)
            sobel.save(name)

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
    p = Preview(IP, width=320, height=240)
    pyglet.app.run()
