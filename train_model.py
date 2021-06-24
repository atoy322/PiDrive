from chainer import Chain
from chainer.links import Linear, Convolution2D
from chainer.functions import relu, mean_squared_error
from chainer.optimizers import Adam
import numpy as np

import dataset


N_ITER = 1000
BATCH_SIZE = 10


class LineDetector(Chain):
    def __init__(self):
        super().__init__()

        with self.init_scope():
            self.conv_1 = Convolution2D(3, 1, 3)
            self.l1 = Linear(1364, 100)
            self.l2 = Linear(100, 3)

    def forward(self, x):
        h = relu(self.conv_1(x))
        h = relu(self.l1(h))
        y = self.l2(h)
        return y


if __name__ == "__main__":
    X, t = dataset.load("Line.dataset")
    X = X.transpose(0, 3, 1, 2) # (N, 24, 64, 3) -> (N, 3, 24, 64)
    print(X.shape)

    model = LineDetector()
    adam = Adam()
    adam.setup(model)

    for i in range(N_ITER):
        model.cleargrads()

        batch_mask = np.random.choice(X.shape[0], 10)
        X_batch = X[batch_mask]
        t_batch = t[batch_mask]

        y_batch = model(X_batch)

        loss = mean_squared_error(y_batch, t_batch)
        print(loss.array)

        loss.backward()
        adam.update()

    from ptpython.repl import embed
    embed(globals(), locals())
