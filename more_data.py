import numpy as np
import cv2
import matplotlib.pyplot as plt
import joblib



def add_noise(img):
    img_ = img.copy()
    noise = np.random.randn(*img_.shape)
    img_ += noise * 5

    img_ -= img_.min()
    img_ /= img_.max()
    img_ *= 255

    return img_


def blur(img):
    img_ = img.copy()

    for i in range(img.shape[0]):
        img_[i] = cv2.blur(img_[i], (3, 3))
    
    img_ -= img_.min()
    img_ /= img_.max()
    img_ *= 255

    return img_



X, y = joblib.load("Line4.dataset")
X = np.array(X, dtype=np.float32)
y = np.array(y)
Xb = blur(X)
Xn = add_noise(X)
print(X.shape, y.shape)
X = np.concatenate([X, Xb, Xn])
y = np.concatenate([y, y, y])

print(X.max(), X.min(), Xb.max(), Xb.min(), Xn.max(), Xn.min())

joblib.dump([X, y], "LineX3.dataset")
