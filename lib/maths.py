
def test_maths():
    print(evalfunc("x**2 + y**2", 'x, y', 7, 2))

def sign(val):
    if val < 0:
        return '-'
    else:
        return '+'

def sgn(val):
    return 1 if val >= 0 else -1    

def evalfunc(f, varstr, *vals):
    vars = varstr.split(",")
    i = 0
    for var in vars:
        f = f.replace(var, str(vals[i]))
        i += 1
    return eval(f)

if __name__ == '__main__':
    test_maths()