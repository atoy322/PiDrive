from chainer.functions import mean_squared_error, accuracy
from chainer.optimizers import Adam
from chainer.serializers import save_npz
import numpy as np
import matplotlib.pyplot as plt

import dataset
from model import LineDetector


N_ITER = 10000
BATCH_SIZE = 30


if __name__ == "__main__":
    X, t = dataset.load("Line0.dataset") # Line2, 3
    X_test, t_test = dataset.load("Line4.dataset") # for test
    #t/=24
    #t_test/=24
    X = X.transpose(0, 3, 1, 2) # (N, 24, 64, 3) -> (N, 3, 24, 64)
    X_test = X_test.transpose(0, 3, 1, 2) # (N, 24, 64, 3) -> (N, 3, 24, 64)
    print(X.shape)

    losses = []
    losses_test = []

    model = LineDetector()
    adam = Adam()
    adam.setup(model)

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

            if not i % BATCH_SIZE:
                print("Train Loss: {:5.4f},  Test Loss: {:5.4f}".format(loss.array, loss_test.array))
                losses.append(loss.array)
                losses_test.append(loss_test.array)

            loss.backward()
            adam.update()
        except KeyboardInterrupt:
            break

    save_npz("model.npz", model)
    plt.plot(losses)
    plt.plot(losses_test)
    plt.show()
    #from ptpython.repl import embed
    #embed(globals(), locals())
