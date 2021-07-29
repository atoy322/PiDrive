from chainer import Chain
from chainer.links import Linear, Convolution2D
from chainer.functions import relu, dropout, max_pooling_2d
 
class LineDetector(Chain):
    def __init__(self):
        super(LineDetector, self).__init__()
 
        with self.init_scope():
            self.l1 = Linear(64*24, 100)
            self.l2 = Linear(100, 100)
            self.l3 = Linear(100, 3)
 
    def forward(self, x):
        h = relu(self.l1(x))
        #h = dropout(h)
        h = relu(self.l2(h))
        #h = dropout(h)
        y = self.l3(h)
        return y