import cv2
from chainer.serializers import load_npz
import numpy as np

from model2 import LineDetector
from dataset import load


def togray(imgs):
    n, h, w, _ = imgs.shape
    buf = np.zeros((n, 1, h, w), dtype=np.float32)
    
    for idx, img in enumerate(imgs):
        buf[idx][0] = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    return buf.copy()

model = LineDetector()
load_npz("model.npz", model)
X, _ = load("Line3.dataset")
x = togray(X)
print(x.shape)
#x = x.transpose(0, 3, 1, 2)
y = model(x)

i = 0

print(X.max(), y.array.max())

while True:
    img = X[i]
    print(y[i])
    img = cv2.resize(img, (640, 240))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.circle(img, (int(y[i][0].array*10), 20*10), 10, (0, 0, 255), -1)
    img = cv2.circle(img, (int(y[i][1].array*10), 12*10), 10, (0, 0, 255), -1)
    img = cv2.circle(img, (int(y[i][2].array*10), 4*10), 10, (0, 0, 255), -1)

    cv2.imshow("", img)
    key = cv2.waitKey()
    if key == 13: break
    if key == ord("n"): i += 1
    if i > len(X)-1: i = 0

cv2.destroyAllWindows()