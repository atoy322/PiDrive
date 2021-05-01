import pickle
import time

import numpy as np
from torch.nn import Module, Linear, CrossEntropyLoss
from torch.optim import Adam
from torch import Tensor, LongTensor, FloatTensor



class TestModel(Module):
    def __init__(self):
        super().__init__()
        self.layer_1 = Linear(4, 10)
        self.layer_2 = Linear(10, 4)

    def forward(self, x):
        h = self.layer_1(x)
        y = self.layer_2(h)
        return y


if __name__ == "__main__":
    with open("iris.npy", "rb") as f:
        X_train, X_test, y_train, y_test = pickle.load(f)

    X_train = Tensor(X_train)
    X_test = Tensor(X_test)
    y_train = Tensor(y_train).type(LongTensor)
    y_test = Tensor(y_test).type(LongTensor)

    model = TestModel()
    opt = Adam(model.parameters())
    loss_func = CrossEntropyLoss()

    for i in range(1000):
        model.zero_grad()
        batch_mask = Tensor(np.random.choice(X_train.shape[0], 10)).type(LongTensor)
        X_batch = X_train[batch_mask]
        y_batch = y_train[batch_mask]

        t1 = time.time()
        output = model(X_train)
        t2 = time.time()

        loss = loss_func(output, y_train)
        loss.backward()
        opt.step()

        print("\rLoss: {:.3f},  Waste: {:.10f}[s]".format(loss, t2-t1), end="")


