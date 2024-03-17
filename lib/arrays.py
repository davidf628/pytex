
def test_arrays():
    a = [1, 2, 3, 4, -1, 0, 15]
    print(calconarray(a, "x + 4"))

def calconarray(array, func):
    return list(map(lambda x: eval(func), array))
    # for i in range(0, len(array)):
    #     evalstr = func.replace('x', str(array[i]))
    #     array[i] = eval(evalstr)
    # return array

if __name__ == '__main__':
    test_arrays()