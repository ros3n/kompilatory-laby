from numpy.core.umath import pi
from numpy.ma import sin, arange
import matplotlib.pyplot as plt
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised import BackpropTrainer

__author__ = 'tomi'

fun = [(x, sin(x)) for x in arange(-pi, pi, pi/10)]

net = buildNetwork(1, 10, 1)

data = SupervisedDataSet(1, 1)
for (x, sinx) in fun:
    data.addSample([x], [sinx])

trainer = BackpropTrainer(net, data, momentum=0.99)

for y in xrange(750):
    trainer.train()

result = [net.activate([x]) for x in arange(-pi, pi, pi/30)]

plt.plot(result)
plt.show()
