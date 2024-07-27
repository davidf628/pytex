import random
import math
from lib.misc import is_number

def test():
    print(rand(1000, 2000, prec=100))


def seed(val):
    random.seed(val)


def rand(min, max, prec=1):
    min = float(min)
    max = float(max)
    dec = 0 if prec == 1 else len(str(prec)) - 2
    lowval = math.floor(min / prec)
    highval = math.floor(max / prec)
    return round(random.randint(lowval, highval) * prec, dec)


def rands(min, max, n, prec=1):
    values = []
    for _ in range(0, n):
        values.append(rand(min, max, prec))
    return values


def diffrands(min, max, n, prec=1):
    rands = []
    for _ in range(0, n):
        value = rand(min, max, prec)
        while value in rands:
            value = rand(min, max, prec)
        rands.append(value)
    return rands


def nzrand(min, max, prec=1):
    rval = rand(min, max, prec)
    while abs(rval) < prec:
        rval = rand(min, max, prec)
    return rval


def nzrands(min, max, n, prec=1):
    rands = []
    for _ in range(0, n):
        rands.append(nzrand(min, max, prec))
    return rands


def nzdiffrands(min, max, n, prec=1):
    rands = []
    for _ in range(0, n):
        value = nzrand(min, max, prec)
        while value in rands:
            value = nzrand(min, max, prec)
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