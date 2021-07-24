import sys

import cv2
import numpy as np

import dataset

if len(sys.argv[1:]) == 0:
    print("Given argument is not enough to run this program.")
    sys.exit()

X, y = dataset.load(sys.argv[1], False)
X = np.array(X)
y = np.array(y)

i = 0

while True:
    img = X[i] / 255
    print("{:4d} / {:4d}".format(i+1, X.shape[0]))
    img = cv2.resize(img, (640, 240))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.circle(img, (int(y[i][0])*10, 20*10), 10, (0, 0, 255), -1)
    img = cv2.circle(img, (int(y[i][1])*10, 12*10), 10, (0, 0, 255), -1)
    img = cv2.circle(img, (int(y[i][2])*10, 4*10), 10, (0, 0, 255), -1)

    cv2.imshow("", img)
    key = cv2.waitKey()
    if key == 13: break
    if key == ord("n"): i += 1
    if i > len(X)-1: i = 0

cv2.destroyAllWindows()