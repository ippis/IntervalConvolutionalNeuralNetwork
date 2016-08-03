from intpy import *

def ErroAbsoluto(xk, xi):
    print("Erro Absoluto: " + str(abs(xk - (xi.middle()))) + " < " + str((xi.diameter()/2)))
def absolutError(xreal,xinterval):
    x = 0.0
    y = 0.0

    x = abs(xreal - (xinterval.middle()))
    y = (xinterval.diameter())/2.0

    return x,y


def ErroRelativo(xk, xi):
    print("Erro Relativo: " + str(abs((xk - xi.middle())/xk)) + " <= " + str((xi.diameter()/(2*xi.inf))))

def relativeError(xreal,xinterval):
    if(xreal == 0.0):
        return 0.0,0.0
    x = abs((xreal - xinterval.middle())/xreal)
    y = (xinterval.diameter())/(2*xinterval.inf)
    return x,y
#print dunif(0.0, 3.0, 1.0, 2.0)
