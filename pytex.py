import sys, re
from lib import *

debugging = False

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

        i += 1 # advance past the variable declaration
        stack = [] # start a new stack for where blocks

        # keeps track of how many times a 'where' command has been called in
        #  order to stop processing at 200 times, which prevents infinite loops
        repeatcounter = {}

        while not isEndVariableSet(data[i]):

            command = uncommentLine(data[i])

            if command.strip() == '{': # begin a 'where' block
                stack.insert(0, i) # save the location of the start of the block
                i += 1

            elif 'where' in command:
                command, condition = command.split('where')

                if command.strip() == '}':
                    blockstart = stack.pop(0)
                    
                else:
                    blockstart = i
                    exec(command)

                if blockstart in repeatcounter.keys():
                    repeatcounter[blockstart] += 1
                    if repeatcounter[blockstart] >= 200:
                        print(f'ERROR "where" condition not met in 200 iterations:\n ==> {i+1}: {uncommentLine(data[i])}')
                        quit()
                else:
                    repeatcounter[blockstart] = 0

                # print(f'count == {repeatcounter[blockstart]}, stack == {stack}, condition == {condition}')

                try:
                    wheremet = eval(condition)
                except Exception as e:
                    print(f'ERROR on line {i+1}: {uncommentLine(data[i])}\n ==> {e}')
                    quit()

                if not wheremet:
                    i = blockstart
                else:
                    i += 1

            else:
                try:
                    exec(command)
                    i += 1
                except Exception as e:
                    print(f'ERROR on line {i+1}: {command}\n ==> {e}')
                    quit()

        i += 1    

    # if a line is not a variable declaraion, see if it contains any
    #  variables to substitute   
    elif hasPython(data[i]):
        while hasPython(data[i]):
            snippet = getPython(data[i])
            try:
                result = eval(snippet)
                data[i] = strsub(snippet, result, data[i])
            except Exception as e:
                print(f'ERROR on line {i+1}: {data[i]}\n ==> {e}')
                quit()

    else:
        i += 1

data = removeVariableDeclarations(data)

with open(outputfile, 'w') as f:
    for line in data:
        f.write(line)

