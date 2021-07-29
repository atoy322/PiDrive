from chainer import Chain
from chainer.links import Linear, Convolution2D
from chainer.functions import relu, dropout, max_pooling_2d
 
class LineDetector(Chain):
    def __init__(self):
        super(LineDetector, self).__init__()
 
        with self.init_scope():
            self.l1 = Convolution2D(1, 3, 3)
            self.l2 = Linear(504, 100)
            self.l3 = Linear(100, 50)
            self.l4 = Linear(50, 3)
 
    def forward(self, x):
        h = relu(self.l1(x))
        h = max_pooling_2d(h, 3)
        h = dropout(h)
        h = relu(self.l2(h))
        #h = dropout(h)
        h = relu(self.l3(h))
        #h = dropout(h)
        y = self.l4(h)
        return y