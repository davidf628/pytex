import sys, os
from lib.misc import __internal_declarations
from lib import *
import lib.cmdline

# for debugging, uncomment this line
sys.argv.append('test.tex')

__version = '0.30.0'

# https://www.myopenmath.com/help.php?section=writingquestions

# https://www.myopenmath.com/assessment/libs/libhelp.php
    
__parseinfo = lib.cmdline.parseCommandLine(sys.argv, __version)

if os.path.isfile(__parseinfo['filename']):
    if not 'outputfilename' in __parseinfo.keys():
        __parseinfo['outputfilename'] = f'out_{__parseinfo["filename"]}'

# Read the .tex file specified from the command line and load it

__data = []

with open(__parseinfo['filename'], "r") as f:
    for __line in f:
        __data.append(__line)

# read through the document looking for variable declarations
__lcv = 0
while (__lcv < len(__data)):

    # search for variable declarations
    if isNewPythonCommands(__data[__lcv]):

        __lcv += 1 # advance past the variable declaration
        __stack = [] # start a new stack for where blocks

        # keeps track of how many times a 'where' command has been called in
        #  order to stop processing at 200 times, which prevents infinite loops
        __rptcounter = {}

        while not isEndPythonCommands(__data[__lcv]):

            __command = uncommentLine(__data[__lcv])

            if __command.strip() == '{': # begin a 'where' block
                __stack.insert(0, __lcv) # save the location of the start of the block
                __lcv += 1

            elif 'where' in __command:
                __command, condition = __command.split('where')

                if __command.strip() == '}':
                    __blockstart = __stack.pop(0)
                    
                else:
                    __blockstart = __lcv
                    variables = extract_variable_names(__command)
                    for variable in variables:
                        if variable in __internal_declarations:
                            print(f'ERROR on line {__lcv+1}: {__command}\n ==> "{variable}" is a reserved word or the name of a function and cannot be used as a variable name.')
                            quit()
                    exec(__command)

                if __blockstart in __rptcounter.keys():
                    __rptcounter[__blockstart] += 1
                    if __rptcounter[__blockstart] >= 200:
                        print(f'ERROR "where" condition not met in 200 iterations:\n ==> {__lcv+1}: {uncommentLine(__data[__lcv])}')
                        quit()
                else:
                    __rptcounter[__blockstart] = 0

                # print(f'count == {__rptcounter[__blockstart]}, __stack == {__stack}, condition == {condition}')

                try:
                    wheremet = eval(condition)
                except Exception as e:
                    print(f'ERROR on line {__lcv+1}: {uncommentLine(__data[__lcv])}\n ==> {e}')
                    quit()

                if not wheremet:
                    __lcv = __blockstart
                else:
                    __lcv += 1

            else:
                try:
                    variables = extract_variable_names(__command)
                    for variable in variables:
                        if variable in __internal_declarations:
                            print(f'ERROR on line {__lcv+1}: {__command}\n ==> "{variable}" is a reserved word or the name of a function and cannot be used as a variable name.')
                            quit()
                    exec(__command)
                    __lcv += 1
                except Exception as e:
                    print(f'ERROR on line {__lcv+1}: {__command}\n ==> {e}')
                    quit()

        __lcv += 1    

    # if a line is not a variable declaraion, see if it contains any
    #  variables to substitute   
    elif hasPython(__data[__lcv]):
        while hasPython(__data[__lcv]):
            __snippet = getPython(__data[__lcv])
            try:
                __result = eval(__snippet)
                __data[__lcv] = strsub(__snippet, __result, __data[__lcv])
            except Exception as e:
                print(f'ERROR on line {__lcv+1}: {__data[__lcv]}\n ==> {e}')
                quit()

    else:
        __lcv += 1

__data = removeVariableDeclarations(__data)

# add the seed information

# write the output .tex file
with open(__parseinfo['outputfilename'], 'w') as __f:
    for __line in __data:
        __f.write(__line)

# create the pdf version

# modify "iskey" flag if necessary and create a key
