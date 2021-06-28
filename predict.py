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
from chainer import serializers

from raspi_ip import IP
from model import LineDetector
#from dataset import load

W = 320
H = 240

#X, y = load("Line.dataset")
#x = X.transpose(0, 3, 1, 2)
model = LineDetector()
serializers.load_npz("model.npz", model)

def gen_name(dir):
    i = 0
    
    while True:
        if not os.path.exists(dir + "/" + f"img-{i}.jpg"):
            break

        i += 1

    return dir + "/" + f"img-{i}.jpg"

""""
def image_preprocess(img):
    img = img.convert("L")
    array = np.array(img)
    edge = cv2.Canny(array, 100, 100)
    img = Image.fromarray(edge)
    return img.convert("RGB")
"""
def image_preprocess(img):
    img = img.crop((0, img.height//2, img.width, img.height))
    img = img.resize() #################################################
    array = np.array(img, dtype=np.float32)
    y = model(array.reshape(-1, *array.shape).transpose(0, 3, 1, 2))
    print(y)
    return img.convert("RGB")


class Preview(Window):
    def __init__(self, ip, width=720, height=480):
        super().__init__(width=width*2, height=height)
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
        self.img = img.transpose(Image.FLIP_TOP_BOTTOM) # To save
        self.preprocessed = image_preprocess(self.img) # To save
        preprocessed = self.preprocessed.transpose(Image.FLIP_TOP_BOTTOM) # To show

        img = ImageData(W, H, "RGB", img.tobytes("raw", "RGB"))
        preprocessed = ImageData(W, H, "RGB", preprocessed.tobytes("raw", "RGB"))
        img.blit(0, 0)
        preprocessed.blit(W, 0)

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
            #self.img = self.img.crop((0, H//2, W, H)).resize((W//5, H//10))
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
