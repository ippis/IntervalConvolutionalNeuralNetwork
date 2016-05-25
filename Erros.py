from intpy import *

def ErroAbsoluto(xk, xi):
    print("Erro Absoluto: " + str(abs(xk - (xi.middle()))) + " < " + str((xi.diameter()/2)))

def ErroRelativo(xk, xi):
    print("Erro Relativo: " + str(abs((xk - xi.middle())/xk)) + " <= " + str((xi.diameter()/(2*xi.inf))))

#print dunif(0.0, 3.0, 1.0, 2.0)
