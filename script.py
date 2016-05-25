from scipy import misc
import time
import png
import subprocess
import os
import random
import numpy as np
from sklearn.neural_network import MLPClassifier
from initIntervals import *
from Erros import *
from NetConvReal import *
from NetConvInt import *


a = ConvNetReal()
aux = np.random.normal(0,1,9)
filter = []
filter.append(aux)

print "CONV EPOCH = 1 e FILTER = 1"
for i in xrange(5):
    a.load()
    a.evaluateNetConv(filter,1,0.6,3,1,0,1)


print "--------------------------------------------------------------------------"
print "CONV EPOCH = 1 e FILTER = 2"
for i in xrange(5):
    a.load()
    a.evaluateNetConv(filter,3,0.6,3,1,0,1)
print "-------------------------------------------------------------------------"
print "CONV INT EPOCH = 3 E FILTER = 1"
b = ConvNetInterval()

for i in xrange(5):
        b.load()
        b.evaluateNetConv(filter,1,0.6,3,1,0,1)


print "-----------------------------------------------------------------------------"
print "CONV INT EPOCH = 3 e FILTER = 1"
for i in xrange(5):
        b.load()
        b.evaluateNetConv(filter,3,0.6,3,1,0,1)
