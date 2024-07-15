
import math

def test_maths():
    print(f'frac(-22.55) == {frac(-22.55)}')
    print(rnd([1.24, 56.6, 21.2, 15.5]))
    print(rnd(2.28))


def sign(val):
    if val < 0:
        return '-'
    else:
        return '+'


def rnd(val, decimals=0):
    if type(val) == str:
        val = float(val)

    if type(val) == list:
        if decimals == 0:
            return [int(round(i, decimals)) for i in val]
        else:
            return [round(i, decimals) for i in val]

    else:
        val = round(val, decimals)
        if decimals == 0:
            return int(val)
        else:
            return val
        

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


###############################################################################
# Formats a integer using thousands place commas

def prettyint(value):
    if type(value) == str:
        value = int(value)
        
    if type(value) == list:
        values = []
        for item in value:
            if type(item) == str:
                item = int(item)
            values.append('{:,}'.format(item))
        return values
    else:
        return '{:,}'.format(value)

if __name__ == '__main__':
    test_maths()