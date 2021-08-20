from chainer.functions import mean_squared_error
from chainer.optimizers import AdaDelta
from chainer.serializers import save_npz
import numpy as np
import cupy as cp
import matplotlib.pyplot as plt
import cv2
 
import dataset
from model import LineDetector


N_ITER = 5000
BATCH_SIZE = 30

def togray(imgs):
  n, h, w, _ = imgs.shape
  buf = np.zeros((n, 1, h, w), dtype=np.float32)

  for idx, img in enumerate(imgs):
    buf[idx][0] = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

  return buf.copy()

X, t = dataset.load("train_data/Line.dataset")
X_test, t_test = dataset.load("train_data/old/Line.dataset") # for test

X = togray(X)
X_test = togray(X_test)

#t /= 64
#t_test /= 64

X = cp.array(X)
t = cp.array(t)
X_test = cp.array(X_test)
t_test = cp.array(t_test)

losses = []
losses_test = []

model = LineDetector()
opt = AdaDelta()
opt.setup(model)

model.to_gpu()


for i in range(N_ITER):
    try:
        model.cleargrads()
 
        batch_mask = np.random.choice(X.shape[0], BATCH_SIZE)
        batch_mask_test = np.random.choice(X_test.shape[0], BATCH_SIZE)
        X_batch = X[batch_mask]
        t_batch = t[batch_mask]
        X_batch_test = X_test[batch_mask_test]
        t_batch_test = t_test[batch_mask_test]
 
        y_batch = model(X_batch)
        y_batch_test = model(X_batch_test)
 
        loss = mean_squared_error(y_batch, t_batch)
        loss_test = mean_squared_error(y_batch_test, t_batch_test)
 
        if not i % (X.shape[0] // BATCH_SIZE):
            print("\rTrain Loss: {:5.4f},  Test Loss: {:5.4f}".format(loss.array, loss_test.array), end="")
            losses.append(loss.array)
            losses_test.append(loss_test.array)
 
        loss.backward()
        opt.update()

    except KeyboardInterrupt:
        break


model.to_cpu()
save_npz("model.npz", model)
plt.xlabel("Epochs")
plt.ylabel("mean squared error (MSE)")
plt.grid(linestyle="--")
plt.plot(losses, label="train", linewidth=0.7)
plt.plot(losses_test, label="test", linewidth=0.7)
plt.legend()
plt.show()
