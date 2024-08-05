
import math

def test_maths():

    print(towords(21))

    for i in range(0, 100):
        print(f'i == {i}, {towords(i)}')


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


###############################################################################
# Writes a number out in an equivalent statment in English

def towords(value):
    value_str = str(value)
    ones = { '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
             '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine' }
    teens = { '10': 'ten', '11': 'eleven', '12': 'twelve', '13': 'thirteen',
              '14': 'fourteen', '15': 'fifteen', '16': 'sixteen', 
              '17': 'seventeen', '18': 'eighteen', '19': 'nineteen' }
    tens = { '10' : 'ten', '20': 'twenty', '30': 'thirty', '40': 'fourty',
             '50' : 'fifty', '60': 'sixty', '70': 'seventy', '80': 'eighty',
             '90' : 'ninety' }
    
    if value < 0 or value > 99:
        return value_str

    if len(value_str) == 1:
        return ones[value_str]
    elif len(value_str) == 2 and (value > 9) and (value < 20):
        return teens[value_str]
    elif len(value_str) == 2 and (value % 10 == 0):
        return tens[value_str]
    elif len(value_str) == 2:
        tens_place = f'{value_str[0]}0'
        ones_place = value_str[1]
        return f'{tens[tens_place]}-{ones[ones_place]}'
  

if __name__ == '__main__':
    test_maths()