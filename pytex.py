import sys, re
from lib import *
from sympy import latex, factor, expand
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import transformations

debugging = False

if debugging:
    sys.argv.append('test.tex')
    outputfile = f'./output/out_{sys.argv[1]}'
else:
    outputfile = f'./out_{sys.argv[1]}'

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

        #data.pop(i)
        i += 1 # advance past the variable declaration
        stack = [] # start a new stack for where blocks
        count = 0

        while not isEndVariableSet(data[i]):
        # remove all the variables from python and start a new variable scope
        #vars = {}

            #command = uncommentLine(data.pop(i))
            command = uncommentLine(data[i])

            if command.strip() == '{': # begin a 'where' block
                stack.insert(0, i) # save the location of the start of the block
                i += 1

            elif 'where' in command:
                command, condition = command.split('where')

                if command.strip() == '}':
                    count += 1
                    #print(f'count == {count}, stack == {stack}, condition == {condition}')
                    blockstart = stack.pop()
                else:
                    blockstart = i
                    #print(f'count == {count}, stack == {stack}, condition == {condition}')
                    exec(command)

                wheremet = eval(condition)
                #print(f'wheremet == {wheremet}')

                if not wheremet:
                    i = blockstart
                else:
                    i += 1

            elif re.search(r'(.*)\=(.*)\?(.*)\:(.*)', command) != None:
                result = re.search(r'(.*)\=(.*)\?(.*)\:(.*)', command)
                variable = result.group(1)
                test = result.group(2)
                iftrue = result.group(3)
                iffalse = result.group(4)
                if eval(test) == True:
                    exec(f'{variable}={iftrue}')
                else:
                    exec(f'{variable}={iffalse}')
                i += 1

            else:
                exec(command)
                i += 1

        i += 1
        #data.pop(i) # remove %end line
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
            #print(data[i])
        # while re.search(r'@\s*([A-Za-z_]\w*)\s*@', data[i]):
        #     result = re.search(r'@\s*([A-Za-z_]\w*)\s*@', data[i])
        #     variable_name = result.group(1)
        #     data[i] = re.sub(r'@\s*' + variable_name + r'\s*@', str(vars[variable_name]), data[i])
        #     print(data[i])
    else:
        i += 1

with open(outputfile, 'w') as f:
    for line in data:
        f.write(line)

