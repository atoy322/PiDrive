import socket
import struct
import io
import os
import math

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


W = 320
H = 240

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
    img_array = np.array(img)
    img_ = img.crop((0, img.height//2, img.width, img.height)).convert("L")
    img_ = img_.resize((64, 24))
    X = np.array(img_, dtype=np.float32)
    X = X.reshape(1, 1, *X.shape) / 255
    y = model(X)[0].array * 5
    m = (20*5 - 12*5) / (y[1] - 32*5) # xの変化量分のyの変化量
    theta = math.atan(m) 
    theta = math.degrees(theta)
    if theta >= 0:
        theta = 90 - theta
    else:
        theta = -(90 + theta)
    color = (167, 254, 113)
    img_array = cv2.circle(img_array, (y[0], 20*5 + 120), 5, color, -1)
    img_array = cv2.circle(img_array, (y[1], 12*5 + 120), 5, color, -1)
    img_array = cv2.circle(img_array, (y[2], 4*5 + 120), 5, color, -1)
    return Image.fromarray(img_array), theta


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
        self.img = img.transpose(Image.FLIP_TOP_BOTTOM) # To save
        self.preprocessed, pred = image_preprocess(self.img) # To save
        preprocessed = self.preprocessed.transpose(Image.FLIP_TOP_BOTTOM) # To show

        img = ImageData(W, H, "RGB", preprocessed.tobytes("raw", "RGB"))
        img.blit(0, 0)

        pred = min(30, max(pred*0.3, -30))
        self.control_sock.send(b"SPEED:40")
        self.control_sock.send(f"STEER:{int(pred)}".encode())

        self.set_caption("FPS: {:3.5f} [frame/s]".format(1/dt))

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

    def on_close(self):
        self.control_sock.send(b"SPEED:0")
        super().on_close()


if __name__ == "__main__":
    print(IP)
    p = Preview(IP, width=W, height=H)
    pyglet.app.run()
