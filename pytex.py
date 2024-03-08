import sys, re, random

sys.argv.append('test.tex')

def rand(min, max):
    return random.randint(min, max)

def rrand(min, max, prec):
    dec = len(str(prec)) - 2
    lowval = round(min / prec, dec)
    highval = round(max / prec, dec)
    return round(random.randint(lowval, highval) * prec, dec)

def nonzerorand(min, max):
    rval = random.randint(min, max)
    while rval != 0:
        rval = random.randint(min, max)
    return rval

def nonzerorrand(min, max, prec):
    rval = rrand(min, max, prec)
    while rval != 0:
        rval = rrand(min, max, prec)
    return rval

def randfrom(values):
    pass

def rands(min, max, n, order='none'):
    pass

def rrands(min, max, prec, n, order='none'):
    pass

def nonzerorands(min, max, n, order='none'):
    pass

def nonzerorrands(min, max, n, order='none'):
    pass

def randsfrom(values, n, order='none'):
    pass

def diffrands(min, max, n, order='none'):
    pass

def diffrandsfrom(values, n, order='none'):
    pass

def nonzerodiffrands(min, max, n, order='none'):
    pass

def nonzerodiffrrands(min, max, prec, n, order='none'):
    pass

# Read the .tex file specified from the command line and load it

filename = sys.argv[1]
data = []

with open(filename, "r") as f:
    for line in f:
        data.append(line)

eod = 0 # End of TeX document, i.e. the line where \end{document} occurs
# skip over all lines until the end of the TeX document
for line_no, line in enumerate(data):
    if re.search(r'\\end\s*\{document\}', line):
        eod = line_no

# start reading in the different variables and begin the randomization
vars = {}
for i in range(eod+1, len(data)):
    if data[i].strip() != '': # skip empty lines
        result = re.search(r'([A-Za-z_]\w*)\s*=\s*(.*)', data[i])
        if result:
            vars[result.group(1)] = eval(result.group(2)) # save a record of the variable
            exec(f'{result.group(1)} = {vars[result.group(1)]}') # put the variable and its value into memory
print(vars)

# replace all the locations of the variables within the TeX document

for i in range(0, eod):
    while re.search(r'@\s*([A-Za-z_]\w*)\s*@', data[i]):
        result = re.search(r'@\s*([A-Za-z_]\w*)\s*@', data[i])
        variable_name = result.group(1)
        print(f'var == {variable_name} val == {vars[variable_name]}')
        data[i] = re.sub(r'@\s*' + variable_name + r'\s*@', str(vars[variable_name]), data[i])
        print(data[i])

with open(f'out_{sys.argv[1]}', 'w') as f:
    for i in range(0, eod+1):
        f.write(data[i])

