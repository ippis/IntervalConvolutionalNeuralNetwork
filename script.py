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
from NetConvRealScript import *
from NetConvIntScript import *



aux = np.random.normal(0,1,9)
filter = []
filter.append(aux)
print filter

print "CONV EPOCH = 1 e FILTER = 1"
for i in xrange(1):
    a = ConvNetReal();
    a.load()
    a.evaluateNetConv(filter,1,0.6,"arq1.txt",3,1,0,1)
    a = None


print "--------------------------------------------------------------------------"
print "CONV EPOCH = 1 e FILTER = 2"

#for i in xrange(5):
#    a.load()
#    a.evaluateNetConv(filter,3,0.6,3,1,0,1)

print "-------------------------------------------------------------------------"
print "CONV INT EPOCH = 1 E FILTER = 1"

filter =[]
filter.append(initInterval(aux,0.00000000001))

for i in xrange(1):
        b = ConvNetInterval()
        b.load()
        b.evaluateNetConv(filter,1,0.6,"arq1.txt",3,1,0,1)
        b = None
