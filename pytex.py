import sys, re
from lib import *

debugging = False

# https://www.myopenmath.com/help.php?section=writingquestions

# https://www.myopenmath.com/assessment/libs/libhelp.php

if debugging:
    sys.argv.append('test.tex')
    outputfile = f'./output/out_{sys.argv[1]}'
else:
    outputfile = f'./out_{sys.argv[1]}'

# Read the .tex file specified from the command line and load it

filename = sys.argv[1]
__data = []

with open(filename, "r") as f:
    for line in f:
        __data.append(line)

# read through the document looking for variable declarations
__lcv = 0
while (__lcv < len(__data)):

    if re.search(r'\\newquestion', line):
        __debugvar = 15

    # search for variable declarations
    if isNewPythonCommands(__data[__lcv]):

        __lcv += 1 # advance past the variable declaration
        stack = [] # start a new stack for where blocks

        # keeps track of how many times a 'where' command has been called in
        #  order to stop processing at 200 times, which prevents infinite loops
        repeatcounter = {}

        while not isEndPythonCommands(__data[__lcv]):

            command = uncommentLine(__data[__lcv])

            if command.strip() == '{': # begin a 'where' block
                stack.insert(0, __lcv) # save the location of the start of the block
                __lcv += 1

            elif 'where' in command:
                command, condition = command.split('where')

                if command.strip() == '}':
                    blockstart = stack.pop(0)
                    
                else:
                    blockstart = __lcv
                    variables = extract_variable_names(command)
                    for variable in variables:
                        if variable in internal_declarations:
                            print(f'ERROR on line {__lcv+1}: {command}\n ==> "{variable}" is a reserved word or the name of a function and cannot be used as a variable name.')
                            quit()
                    exec(command)

                if blockstart in repeatcounter.keys():
                    repeatcounter[blockstart] += 1
                    if repeatcounter[blockstart] >= 200:
                        print(f'ERROR "where" condition not met in 200 iterations:\n ==> {__lcv+1}: {uncommentLine(__data[__lcv])}')
                        quit()
                else:
                    repeatcounter[blockstart] = 0

                # print(f'count == {repeatcounter[blockstart]}, stack == {stack}, condition == {condition}')

                try:
                    wheremet = eval(condition)
                except Exception as e:
                    print(f'ERROR on line {__lcv+1}: {uncommentLine(__data[__lcv])}\n ==> {e}')
                    quit()

                if not wheremet:
                    __lcv = blockstart
                else:
                    __lcv += 1

            else:
                try:
                    variables = extract_variable_names(command)
                    for variable in variables:
                        if variable in internal_declarations:
                            print(f'ERROR on line {__lcv+1}: {command}\n ==> "{variable}" is a reserved word or the name of a function and cannot be used as a variable name.')
                            quit()
                    exec(command)
                    __lcv += 1
                except Exception as e:
                    print(f'ERROR on line {__lcv+1}: {command}\n ==> {e}')
                    quit()

        __lcv += 1    

    # if a line is not a variable declaraion, see if it contains any
    #  variables to substitute   
    elif hasPython(__data[__lcv]):
        while hasPython(__data[__lcv]):
            snippet = getPython(__data[__lcv])
            try:
                result = eval(snippet)
                __data[__lcv] = strsub(snippet, result, __data[__lcv])
            except Exception as e:
                print(f'ERROR on line {__lcv+1}: {__data[__lcv]}\n ==> {e}')
                quit()

    else:
        __lcv += 1

__data = removeVariableDeclarations(__data)

with open(outputfile, 'w') as f:
    for line in __data:
        f.write(line)