import sys, re
from lib import *

sys.argv.append('test.tex')

# Read the .tex file specified from the command line and load it

filename = sys.argv[1]
data = []

with open(filename, "r") as f:
    for line in f:
        data.append(line)

# read through the document looking for variable declarations
i = 0
while (i < len(data)):
    line = data[i]

    if re.search(r'\\newquestion', line):
        __debugvar = 15

    # search for variable declarations
    if re.search(r'\s*^\%\s*variables\s*$', line, re.IGNORECASE):
        vars = {} # start a new variable "scope"
        i += 1 # advance to next line
        while data[i].strip() == '': # skip any blank lines
            i += 1
        result = re.search(r'\s*\%\s*([A-Za-z_]\w*)\s*=\s*(.*)', data[i])
        while result: # the current line depicts a variable declaration
            expr = subvars(result.group(2), vars)
            vars[result.group(1)] = eval(expr) # save a record of the variable 
            i += 1 # advance to next line
            while data[i].strip() == '': # skip any blank lines
                i += 1
            result = re.search(r'\s*\%\s*([A-Za-z_]\w*)\s*=\s*(.*)', data[i])
        i -= 1       

    # if a line is not a variable declaraion, see if it contains any
    #  variables to substitute   
    else:
        while re.search(r'@\s*([A-Za-z_]\w*)\s*@', data[i]):
            result = re.search(r'@\s*([A-Za-z_]\w*)\s*@', data[i])
            variable_name = result.group(1)
            data[i] = re.sub(r'@\s*' + variable_name + r'\s*@', str(vars[variable_name]), data[i])
            print(data[i])
    i += 1

with open(f'./output/out_{sys.argv[1]}', 'w') as f:
    for line in data:
        f.write(line)

