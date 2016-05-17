from intpy import *
from math import sqrt

def initInterval(vetor,delta):
    vetorI = list();
    for i in range(len(vetor)):
        vetorI.append(IReal(vetor[i]) + IReal(-delta,delta))
    return vetorI

def sqrtI(dado):
    result = IReal(sqrt(dado.inf), sqrt(dado.sup))
    
    return result

def powI(dado, exp):
    result = IReal(dado.inf**exp, dado.sup**exp)
    
    return result
    
