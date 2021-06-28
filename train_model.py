from chainer.functions import mean_squared_error, accuracy
from chainer.optimizers import Adam
from chainer.serializers import save_npz
import numpy as np

import dataset
from model import LineDetector


N_ITER = 7000
BATCH_SIZE = 10


if __name__ == "__main__":
    X, t = dataset.load("Line2.dataset")
    t/=24
    X = X.transpose(0, 3, 1, 2) # (N, 24, 64, 3) -> (N, 3, 24, 64)
    print(X.shape)

    model = LineDetector()
    adam = Adam()
    adam.setup(model)

    for i in range(N_ITER):
        try:
            model.cleargrads()

            batch_mask = np.random.choice(X.shape[0], BATCH_SIZE)
            X_batch = X[batch_mask]
            t_batch = t[batch_mask]

            y_batch = model(X_batch)

            loss = mean_squared_error(y_batch, t_batch)

            if not i % BATCH_SIZE:
                print("Loss: {:5.4f}".format(loss.array))

            loss.backward()
            adam.update()
        except KeyboardInterrupt:
            break

    save_npz("model.npz", model)
    # from ptpython.repl import embed
    # embed(globals(), locals())
