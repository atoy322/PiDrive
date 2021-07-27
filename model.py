from chainer import Chain
from chainer.links import Linear, Convolution2D
from chainer.functions import relu, dropout, max_pooling_2d
 
class LineDetector(Chain):
    def __init__(self):
        super(LineDetector, self).__init__()
 
        with self.init_scope():
            self.conv_1 = Convolution2D(3, 10, 3)
            self.conv_2 = Convolution2D(10, 1, 3)
            self.l1 = Linear(14, 10)
            self.l2 = Linear(10, 3)
 
    def forward(self, x):
        h = relu(self.conv_1(x))
        h = max_pooling_2d(h, 3)
        #h = dropout(h)
        h = relu(self.conv_2(h))
        h = max_pooling_2d(h, 3)
        #h = dropout(h)
        h = relu(self.l1(h))
        #h = dropout(h)
        y = self.l2(h)
        return y