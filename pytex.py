import sys, re
from lib import *

debugging = True

# https://www.myopenmath.com/help.php?section=writingquestions

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

        # keeps track of how many times a 'where' command has been called in
        #  order to stop processing at 200 times, which prevents infinite loops
        repeatcounter = {}
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

                if blockstart in repeatcounter.keys():
                    repeatcounter[blockstart] += 1
                    if repeatcounter[blockstart] >= 200:
                        print(f'where condition {i+1}: "{uncommentLine(data[i])}" not met in 200 iterations')
                        quit()
                else:
                    repeatcounter[blockstart] = 0

                wheremet = eval(condition)
                #print(f'wheremet == {wheremet}')

                if not wheremet:
                    i = blockstart
                else:
                    i += 1

            else:
                try:
                    exec(command)
                    i += 1
                except Exception as e:
                    print(f'ERROR on line {i}: {command}')
                    print(f'\n{e}')
                    quit()

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

data = removeVariableDeclarations(data)

with open(outputfile, 'w') as f:
    for line in data:
        f.write(line)

