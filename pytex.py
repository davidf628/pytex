import sys, re
from lib import *
from sympy import latex, factor, expand
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import transformations

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

    if re.search(r'\\newquestion', line):
        __debugvar = 15

    # search for variable declarations
    if isNewVariableSet(data[i]):

        data.pop(i)
        #i += 1 # advance past the variable declaration

        while not isEndVariableSet(data[i]):
        # remove all the variables from python and start a new variable scope
        #vars = {}

            command = uncommentLine(data.pop(i))

            if 'where' in command:
                command, condition = command.split('where')
                exec(command)
                wheremet = eval(condition)
                count = 0
                while not wheremet and count < 200:
                    exec(command)
                    eval(condition)
                    count += 1
                if count >= 200:
                    print(f'Where condition {condition} not met in 200 iterations.')
                    quit()
            else:
                exec(command)


        
        data.pop(i) # remove %end line
            # advance to next line
            # while data[i].strip() == '': # skip any blank lines
            #     i += 1
            # result = re.search(r'\s*\%\s*([A-Za-z_]\w*)\s*=\s*(.*)', data[i])
            # while result: # the current line depicts a variable declaration

            #     #expr = subvars(result.group(2), vars)
            #     #vars[result.group(1)] = eval(expr) # save a record of the variable 
            #     i += 1 # advance to next line
            #     while data[i].strip() == '': # skip any blank lines
            #         i += 1
            #     result = re.search(r'\s*\%\s*([A-Za-z_]\w*)\s*=\s*(.*)', data[i])
            # i -= 1       

    # if a line is not a variable declaraion, see if it contains any
    #  variables to substitute   
    elif hasPython(data[i]):
        while hasPython(data[i]):
            snippet = getPython(data[i])
            result = eval(snippet)
            data[i] = strsub(snippet, result, data[i])
            #data[i] = re.sub(f'\\@.*?\\@', str(result), data[i], 1)
            print(data[i])
        # while re.search(r'@\s*([A-Za-z_]\w*)\s*@', data[i]):
        #     result = re.search(r'@\s*([A-Za-z_]\w*)\s*@', data[i])
        #     variable_name = result.group(1)
        #     data[i] = re.sub(r'@\s*' + variable_name + r'\s*@', str(vars[variable_name]), data[i])
        #     print(data[i])
    else:
        i += 1

with open(f'./output/out_{sys.argv[1]}', 'w') as f:
    for line in data:
        f.write(line)

