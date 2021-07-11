from chainer import Chain
from chainer.links import Linear, Convolution2D
from chainer.functions import relu

class LineDetector(Chain):
    def __init__(self):
        super().__init__()

        with self.init_scope():
            self.conv_1 = Convolution2D(3, 3, 5)
            self.conv_2 = Convolution2D(3, 1, 5)
            self.l1 = Linear(896, 50)
            self.l2 = Linear(50, 3)

    def forward(self, x):
        h = relu(self.conv_1(x))
        h = relu(self.conv_2(h))
        h = relu(self.l1(h))
        y = self.l2(h)
        return y
