import random
import math
from lib.misc import is_number
from lib.maths import rnd
#from misc import is_number
#from maths import rnd

def test():
    print(rand(15, 25,n=4, prec=0.001))


def seed(val):
    random.seed(val)

###############################################################################
# Private function that chooses a single random number based on a given 
#  minimum and maxmimum value, and to a specific precision. All other numeric
#  randomizers call this function

def __randval(minimum, maximum, prec=1):
    minval = float(minimum)
    maxval = float(maximum)
    decimals = 0 if prec == 1 else len(str(prec)) - 2
    minval = math.floor(minval / prec)
    maxval = math.floor(maxval / prec)
    return rnd(random.randint(minval, maxval) * prec, decimals)


def rand(minimum, maximum, /, prec=1, n=1, diff=True):
    if n == 1:
        return __randval(minimum, maximum, prec=prec)
    else:
        if diff:
            return diffrands(minimum, maximum, n=n, prec=prec)
        else:
            return rands(minimum, maximum, n=n, prec=prec)


def rands(minimum, maximum, n, prec=1):
    values = []
    for _ in range(0, n):
        values.append(__randval(minimum, maximum, prec))
    return values


def diffrands(minimum, maximum, n, prec=1):
    rands = []
    for _ in range(0, n):
        value = __randval(minimum, maximum, prec)
        while value in rands:
            value = __randval(minimum, maximum, prec)
        rands.append(value)
    return rands


def nzrand(minimum, maximum, prec=1):
    rval = __randval(minimum, maximum, prec)
    while abs(rval) < prec:
        rval = __randval(minimum, maximum, prec)
    return rval


def nzrands(minimum, maximum, n, prec=1):
    rands = []
    for _ in range(0, n):
        rands.append(nzrand(minimum, maximum, prec))
    return rands


def nzdiffrands(minimum, maximum, n, prec=1):
    rands = []
    for _ in range(0, n):
        value = nzrand(minimum, maximum, prec)
        while value in rands:
            value = nzrand(minimum, maximum, prec)
        rands.append(value)
    return rands


def randfrom(values):
    if type(values) == str:
        values = values.split(",")
        values = list(map(lambda x: x.strip(), values))
    selection = random.choice(values)
    if is_number(selection):
        return float(selection)
    else:
        return random.choice(values)


def randsfrom(values, n):
    choices = []
    for _ in range(0, n):
        choices.append(randfrom(values))
    return choices


def diffrandsfrom(values, n):
    rands = []
    for _ in range(0, n):
        value = randfrom(values)
        while value in rands:
            value = randfrom(values)
        rands.append(value)
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

def randsgn():
    return randfrom([-1, 1])


###############################################################################
# When randomly choosing a word from a list, you often need to put 'a' or 'an'
#  before that word in the context of the problem, this chooses the correct
#  indefinite article based on whether the next word begins with a vowel or
#  not.

def indefinitearticle(word):

    word = word.lower()

    aexcep = ['europe', 'european', 'unicorn', 'url', 'eulogy', 'one',
              'once']
    anexcep = ['honor', 'heir', 'hourglass']

    if word in aexcep:
        return 'a'
    elif word in anexcep:
        return 'an'

    if word[0] in ['a', 'e', 'i', 'o', 'u']:
        return 'an'
    else:
        return 'a'

if __name__ == '__main__':
    test()