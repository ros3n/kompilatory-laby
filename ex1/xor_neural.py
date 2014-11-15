from pybrain.supervised.trainers import trainer
import matplotlib.pyplot as plt
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised import BackpropTrainer

net = buildNetwork(2, 2, 1)
data = SupervisedDataSet(2, 1)
data.addSample([1, 1], [0])
data.addSample([1, 0], [1])
data.addSample([0, 1], [1])
data.addSample([0, 0], [0])
data.addSample([1, 1], [0])
data.addSample([1, 0], [1])
data.addSample([0, 1], [1])
data.addSample([0, 0], [0])
data.addSample([1, 1], [0])
data.addSample([1, 0], [1])
data.addSample([0, 1], [1])
data.addSample([0, 0], [0])
data.addSample([1, 1], [0])
data.addSample([1, 0], [1])
data.addSample([0, 1], [1])
data.addSample([0, 0], [0])

trainer = BackpropTrainer(net, data, momentum=0.99)

x = []

for i in xrange(500):
    x.append(trainer.train())

print net.activate([1, 1])
print net.activate([0, 0])
print net.activate([1, 0])
print net.activate([0, 1])

plt.plot(x)
plt.show()

print("Hello!")