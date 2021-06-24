import os

from pyglet.window import Window
from pyglet.window import key
from pyglet.image import ImageData
from pyglet.graphics import Batch
from pyglet.shapes import Circle, Line
from pyglet.text import Label
from pyglet.app import run
from PIL import Image
import numpy as np
import joblib


W = 320
H = 240

DATAPATH = "train_data"
LAYERS = (220, 180, 140)
N = 2
SLIDER_COLOR = (255, 0, 0)
SLIDER_SIZE = 10
TEXT_COLOR = (0, 255, 0, 255)
TEXT_SIZE = 30

EXPORT_PATH = "Line.dataset"


class Maker(Window):
    def __init__(self):
        super().__init__(width=W*N, height=H*N)

        self.position = (0, 0)

        self.index = 0
        self.image = Image.open(DATAPATH + f"/img-{self.index}.jpg")

        self.batch = Batch()

        self.layer_1 = Line(0, self.height-LAYERS[0]*N, self.width, self.height-LAYERS[0]*N, batch=self.batch)
        self.layer_2 = Line(0, self.height-LAYERS[1]*N, self.width, self.height-LAYERS[1]*N, batch=self.batch)
        self.layer_3 = Line(0, self.height-LAYERS[2]*N, self.width, self.height-LAYERS[2]*N, batch=self.batch)

        self.line_1_2 = Line(self.width//2, self.height-LAYERS[0]*N, self.width//2, self.height-LAYERS[1]*N, batch=self.batch)
        self.line_2_3 = Line(self.width//2, self.height-LAYERS[1]*N, self.width//2, self.height-LAYERS[2]*N, batch=self.batch)

        self.slider_1 = Circle(self.width//2, self.height-LAYERS[0]*N, SLIDER_SIZE, color=SLIDER_COLOR, batch=self.batch)
        self.slider_2 = Circle(self.width//2, self.height-LAYERS[1]*N, SLIDER_SIZE, color=SLIDER_COLOR, batch=self.batch)
        self.slider_3 = Circle(self.width//2, self.height-LAYERS[2]*N, SLIDER_SIZE, color=SLIDER_COLOR, batch=self.batch)

        self.slider_1_pressed = False
        self.slider_2_pressed = False
        self.slider_3_pressed = False

        self.label = Label("", "Source Code Pro", TEXT_SIZE, True, color=TEXT_COLOR, x=0, y=self.height-TEXT_SIZE, batch=self.batch)

    def on_draw(self):
        self.clear()
        self.draw_image()
        self.label.text = "{:2d}/{:2d}  ({:3d}, {:3d})".format(self.index+1, len(os.listdir(DATAPATH)), self.position[0]//N, H - self.position[1]//N)
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        r = SLIDER_SIZE // 2
        slider_left = (self.slider_1.x - r, self.slider_2.x - r, self.slider_3.x - r)
        slider_right = (self.slider_1.x + r, self.slider_2.x + r, self.slider_3.x + r)
        slider_top = (self.slider_1.y + r, self.slider_2.y + r, self.slider_3.y + r)
        slider_bottom = (self.slider_1.y - r, self.slider_2.y - r, self.slider_3.y - r)

        if x >= slider_left[0] and x <= slider_right[0] and y >= slider_bottom[0] and y <= slider_top[0]:
            self.slider_1_pressed = True
        elif x >= slider_left[1] and x <= slider_right[1] and y >= slider_bottom[1] and y <= slider_top[1]:
            self.slider_2_pressed = True
        elif x >= slider_left[2] and x <= slider_right[2] and y >= slider_bottom[2] and y <= slider_top[2]:
            self.slider_3_pressed = True

    def on_mouse_release(self, x, y, button, modifiers):
        self.slider_1_pressed = False
        self.slider_2_pressed = False
        self.slider_3_pressed = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.position = (x, y)

        if self.slider_1_pressed:
            self.slider_1.x = x
            self.line_1_2.x = x
        elif self.slider_2_pressed:
            self.slider_2.x = x
            self.line_1_2.x2 = x
            self.line_2_3.x = x
        elif self.slider_3_pressed:
            self.slider_3.x = x
            self.line_2_3.x2 = x

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            print(self.slider_1.x//N, self.slider_2.x//N, self.slider_3.x//N)

            self.index += 1
            if not os.path.exists(DATAPATH + f"/img-{self.index}.jpg"):
                self.index = 0

    def draw_image(self):
        self.image = Image.open(DATAPATH + f"/img-{self.index}.jpg")
        img = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        img = img.resize((self.width, self.height))
        img = ImageData(self.width, self.height, "RGB", img.tobytes("raw", "RGB"))
        img.blit(0, 0)


if __name__ == "__main__":
    maker = Maker()
    run()
