import math

import cv2
from PIL import Image
import numpy as np
from chainer.serializers import load_npz

from model import LineDetector



model = LineDetector()
load_npz("model.npz", model)


def predict(img):
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

cam = cv2.VideoCapture(0)

while True:
    try:
        flag, res = cam.read() # 640 x 480
        if not flag:
            continue

        res = cv2.resize(res, (320, 240))
        image = Image.fromarray(res)
        predict(image[1])
    except Exception as e:
        print(e)
        break

cam.release()