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
    new_index = diffrands(0, len(array)-1, n=len(array))
    new_array = []
    for i in new_index:
        new_array.append(array[i])
    return new_array


# This function randomizes multiple choice answers. The default placement
#  of the original solution is expected to be the 0th index of the array
#  but this can be specified in sol_index if another value is used.
# choice_type is a parameter like '1', 'a', or 'A' indicating what kind
#  of choice lettering is used. If this is specified then the return
#  will the be converted to a index of an array created with this 
#  starting point, relative to the offset of solution_index
# Returns the new array of multiple chioce values and the new index of
#  where the solution is now located

def multiplechoiceshuffle(choices, solution_index=0, choice_type=None):
    solution_value = choices[solution_index]
    choices = singleshuffle(choices)
    solution_index = choices.index(solution_value)
    
    if choice_type != None:
        start_code = ord(choice_type)
        count = len(choices)
        choice_values = [chr(start_code + i) for i in range(count)]
        solution = choice_values[solution_index]
        return choices, solution
    
    return choices, solution_index

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