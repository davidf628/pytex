import random

def test():
    p = rrand(0.01, 0.05, 0.001)
    a = randfrom([ 0.01, 0.05, 0.08, 0.1])
    apct = round(a * 100)
    print(type(p))
    print(type(a))
    exec('p <= a')
    #sol = p <= a ? "a. Reject $H_0$" : "b. Fail to reject $H_0$"

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
    if type(values) == str:
        values = values.split(",")
        values = list(map(lambda x: x.strip(), values))
    return random.choice(values)

def rands(min, max, n, order='none'):
    values = []
    for _ in range(0, n):
        values.append(rand(min, max))
    if order == 'inc':
        values.sort()
    elif order == 'dec':
        values.sort(reverse=True)
    return values

def rrands(min, max, prec, n, order='none'):
    values = []
    for _ in range(0, n):
        values.append(rrand(min, max, prec))
    if order == 'inc':
        values.sort()
    elif order == 'dec':
        values.sort(reverse=True)
    return values

def nonzerorands(min, max, n, order='none'):
    values = []
    for _ in range(0, n):
        new_val = 0
        while new_val == 0:
            new_val = rand(min, max)
        values.append(rand(min, max))
    if order == 'inc':
        values.sort()
    elif order == 'dec':
        values.sort(reverse=True)
    return values

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

def singleshuffle(array):
    i = 0
    while i < len(array):
        swapIndex = rand(0, len(array)-1)
        tmp = array[swapIndex]
        array[swapIndex] = array[i]
        array[i] = tmp
        i += 1
    return array

if __name__ == '__main__':
    test()