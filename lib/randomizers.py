import random

def rand(min, max):
    return random.randint(min, max)

def rrand(min, max, prec):
    dec = len(str(prec)) - 2
    lowval = round(min / prec, dec)
    highval = round(max / prec, dec)
    return round(random.randint(lowval, highval) * prec, dec)

def nonzerorand(min, max):
    rval = random.randint(min, max)
    while rval == 0:
        rval = random.randint(min, max)
    return rval

def nonzerorrand(min, max, prec):
    rval = rrand(min, max, prec)
    while rval == 0:
        rval = rrand(min, max, prec)
    return rval

def randfrom(values):
    pass

def rands(min, max, n, order='none'):
    pass

def rrands(min, max, prec, n, order='none'):
    pass

def nonzerorands(min, max, n, order='none'):
    pass

def nonzerorrands(min, max, n, order='none'):
    pass

def randsfrom(values, n, order='none'):
    pass

def diffrands(min, max, n, order='none'):
    pass

def diffrandsfrom(values, n, order='none'):
    pass

def nonzerodiffrands(min, max, n, order='none'):
    pass

def nonzerodiffrrands(min, max, prec, n, order='none'):
    pass
