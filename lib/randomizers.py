import random

def test():
    print(nonzerodiffrrands(-0.5, 0.5, 0.1, 7))

def seed(val):
    random.seed(val)

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

def nonzerorrands(min, max, prec, n, order='none'):
    values = []
    for _ in range(0, n):
        new_val = 0
        while abs(new_val) < prec:
            new_val = rrand(min, max, prec)
        values.append(new_val)
    if order == 'inc':
        values.sort()
    elif order == 'dec':
        values.sort(reverse=True)
    return values

def randsfrom(values, n, order='none'):
    choices = []
    for _ in range(0, n):
        choices.append(randfrom(values))
    if order == 'inc':
        choices.sort()
    elif order == 'dec':
        choices.sort(reverse=True)
    return choices

def diffrands(min, max, n, order='none'):
    rands = []
    for _ in range(0, n):
        value = rand(min, max)
        while value in rands:
            value = rand(min, max)
        rands.append(value)
    if order == 'inc':
        rands.sort()
    elif order == 'dec':
        rands.sort(reverse=True)
    return rands

def diffrrands(min, max, prec, n, order='none'):
    rands = []
    for _ in range(0, n):
        value = rrand(min, max, prec)
        while value in rands:
            value = rrand(min, max, prec)
        rands.append(value)
    if order == 'inc':
        rands.sort()
    elif order == 'dec':
        rands.sort(reverse=True)
    return rands

def diffrandsfrom(values, n, order='none'):
    rands = []
    for _ in range(0, n):
        value = randfrom(values)
        while value in rands:
            value = randfrom(values)
        rands.append(value)
    if order == 'inc':
        rands.sort()
    elif order == 'dec':
        rands.sort(reverse=True)
    return rands

def nonzerodiffrands(min, max, n, order='none'):
    rands = []
    for _ in range(0, n):
        value = rand(min, max)
        while (value in rands) or (value == 0):
            value = rand(min, max)
        rands.append(value)
    if order == 'inc':
        rands.sort()
    elif order == 'dec':
        rands.sort(reverse=True)
    return rands

def nonzerodiffrrands(min, max, prec, n, order='none'):
    rands = []
    for _ in range(0, n):
        value = rrand(min, max, prec)
        while (value in rands) or (abs(value) < prec):
            value = rrand(min, max, prec)
        rands.append(value)
    if order == 'inc':
        rands.sort()
    elif order == 'dec':
        rands.sort(reverse=True)
    return rands

def singleshuffle(array):
    i = 0
    while i < len(array):
        swapIndex = rand(0, len(array)-1)
        array[swapIndex], array[i] = (array[i], array[swapIndex])
        i += 1
    return array

def jointshuffle(array1, array2):
    i = 0
    while i < len(array1):
        swapIndex = rand(0, len(array1)-1)
        array1[swapIndex], array1[i] = (array1[i], array1[swapIndex])
        array2[swapIndex], array2[i] = (array2[i], array2[swapIndex])
        i += 1
    return [array1, array2]

if __name__ == '__main__':
    test()