
from lib import *
from sympy import latex

def test_arrays():
    a = [1, 2, 3, 4, -1, 0, 15]
    print(joinarray(a, func=lambda x: latex(x)))


def calconarray(array, func, variables={}):
    for varname in variables.keys():
        func = func.replace(varname, str(variables[varname]))
    newarray = array.copy()
    #return list(map(lambda x: eval(func), array))
    for i in range(0, len(array)):
        evalstr = func.replace('x', str(newarray[i]))
        newarray[i] = eval(evalstr)
    return newarray


def sorta(array):
    array.sort()
    return array


def sortd(array):
    array.sort(reverse = True)
    return array


def joinarray(array, separator=", ", func=lambda x: str(x)):
    return separator.join(map(lambda x: func(x), array))


def latexjoinarray(array, separator=", "):
    return joinarray(array, separator=separator, func=lambda x: latex(x))


if __name__ == '__main__':
    test_arrays()