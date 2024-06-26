
import math

def test_maths():
    print(f'frac(-22.55) == {frac(-22.55)}')


def sign(val):
    if val < 0:
        return '-'
    else:
        return '+'


def sgn(val):
    return 1 if val >= 0 else -1    


def frac(val):
    return abs(val) % 1


def reducefraction(num, denom):
    divisor = math.gcd(num, denom)
    return [num // divisor, denom // divisor]


def evalfunc(f, varstr, *vals):
    vars = varstr.split(",")
    i = 0
    for var in vars:
        f = f.replace(var, str(vals[i]))
        i += 1
    return eval(f)

if __name__ == '__main__':
    test_maths()