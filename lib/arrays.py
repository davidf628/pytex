
from lib import *

def test_arrays():
    a = [1, 2, 3, 4, -1, 0, 15]
    print(calconarray(a, "x + 4"))

def calconarray(array, func):
    newarray = array.copy()
    #return list(map(lambda x: eval(func), array))
    for i in range(0, len(array)):
        evalstr = func.replace('x', str(newarray[i]))
        newarray[i] = eval(evalstr)
    return newarray

if __name__ == '__main__':
    test_arrays()