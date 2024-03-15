import random

def test():
    x = [ "95\%", "90\%", "80\%" ]
    choices = [ "a.", "b.", "c." ]
    x = singleshuffle(x)
    ans = x.index("95\%")
    print(f'x == {x}\nchoices == {choices}\nanswer: {choices[ans]}{x[ans]}')

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
        array[swapIndex], array[i] = (array[i], array[swapIndex])
        i += 1
    return array

def jointshuffle(array1, array2):
    i = 0
    while i < len(array1):
        swapIndex = rand(0, len(array1)-1)
        array1[swapIndex], array1[i] = (array1[i], array1[swapIndex])
        array2[swapIndex], array2[i] = (array2[i], array2[swapIndex])
        # tmp1 = array1[swapIndex]
        # tmp2 = array2[swapIndex]
        # array1[swapIndex] = array1[i]
        # array2[swapIndex] = array2[i]
        # array1[i] = tmp1
        # array2[i] = tmp2
        i += 1
    return [array1, array2]

if __name__ == '__main__':
    test()