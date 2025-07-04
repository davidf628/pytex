import sys, os, pathlib, sympy
from lib.misc import __internal_declarations
from lib import *
import lib.cmdline

# for debugging, uncomment these lines
#sys.argv.append('/Users/davidflenner/Library/CloudStorage/OneDrive-CollegeofCharleston/committees/Calculus/Placement/placement_exam/placement_exam.tex')
#sys.argv.append('test.tex')
#sys.argv.append('-v=A')
#sys.argv.append('--seed=12345')
#sys.argv.append('--key')
#sys.argv.append('-o=./output/mytestA.tex')
#sys.argv.append('-r')
#sys.argv.append('-c=q1.tex?n=2?sep=\\item')
#sys.argv.append('-c=/Users/davidflenner/Library/CloudStorage/OneDrive-CollegeofCharleston/committees/Calculus/Placement/placement_exam/questions/fraction-sum-1.tex')

def main():
    args = lib.cmdline.patchArgs(sys.argv)
    
    __version = '0.7.0'

    # https://www.myopenmath.com/help.php?section=writingquestions

    # https://www.myopenmath.com/assessment/libs/libhelp.php
        
    __parseinfo = lib.cmdline.parseCommandLine(args, __version)
    __data = []

    if __parseinfo['repl']:
        print(f'\n\nEnter commands for PyTeX to execute.  Type "done" to run the commands. ',end='')
        print(f'Variables can be declared in %python...%end blocks, and and code to display ',end='')
        print(f'must be in @...@ blocks.\n')
        while True:
            command = input('==> ')
            if command.lower() == 'done':
                break
            else:
                __data.append(command)

        # Execute the PyTeX commands
        __data = __run_pytex_commands(__data)


    elif __parseinfo['compile']:
        __temp = load_pytex_file(__parseinfo['filename'])

        for _ in range(__parseinfo['n']):
            if __parseinfo['sep'] != '':
                __data.append(f'\n{__parseinfo["sep"]}\n') 
            __data += __temp

        # Execute the PyTeX commands
        __data = __run_pytex_commands(__data)
            
    else:
        # Read the .tex file specified from the command line and load it
        __data = load_pytex_file(__parseinfo['filename'])

        # Check for any importpytex statments and process those first
        __data = checkImportStatements(__data)

        # Set the specified version number in the document
        __data = setVersionValue(__data, __parseinfo['version'])

        # Set the make_key flag
        __data = setKeyFlag(__data, __parseinfo['key'])

        # Set the seed for randomization
        exec(f'seed({__parseinfo["seed"]})')

        # Execute the PyTeX commands
        __data = __run_pytex_commands(__data)

        # add the seed information
        __data.insert(0, f"%seed - {__parseinfo['seed']}\n\n")


    # In command line mode, we just output the results, otherwise we write the
    #  results to a file and compile it to a pdf
    if __parseinfo['repl'] or __parseinfo['compile']:
        for __line in __data:
            print(__line, end='')
    else:
        
        # write the output .tex file
        with open(__parseinfo['outputfile'], 'w') as __f:
            for __line in __data:
                __f.write(__line)

        # create the pdf version
        os.system(f'pdflatex "{__parseinfo["outputfile"]}"')

        # remove the scrap files
        if os.path.isfile(__parseinfo['aux']):
            pathlib.Path.unlink(__parseinfo['aux'])
        if os.path.isfile(__parseinfo['log']):
            pathlib.Path.unlink(__parseinfo['log'])
        if os.path.isfile(__parseinfo['gz']):
            pathlib.Path.unlink(__parseinfo['gz'])


def __run_pytex_commands(__data):
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
                                sys.exit(-1)
                        print(f'{__lcv}: {__command}')
                        exec(__command)

                    if __blockstart in __rptcounter.keys():
                        __rptcounter[__blockstart] += 1
                        if __rptcounter[__blockstart] >= 200:
                            print(f'ERROR "where" condition not met in 200 iterations:\n ==> {__lcv+1}: {uncommentLine(__data[__lcv])}')
                            sys.exit(-1)
                    else:
                        __rptcounter[__blockstart] = 0

                    try:
                        wheremet = eval(condition)
                    except Exception as e:
                        print(f'ERROR on line {__lcv+1}: {uncommentLine(__data[__lcv])}\n ==> {e}')
                        sys.exit(-1)

                    if not wheremet:
                        __lcv = __blockstart
                    else:
                        __lcv += 1

                elif is_python_code_block(__command):
                    code_block, block_length = get_python_code_block(__data, __lcv)
                    print(f'{__lcv}: {code_block}')
                    exec(code_block)
                    __lcv += block_length
                
                else:
                    try:
                        variables = extract_variable_names(__command)
                        if len(variables) > 0:
                            for variable in variables:
                                if variable in __internal_declarations:
                                    print(f'ERROR on line {__lcv+1}: {__command}\n ==> "{variable}" is a reserved word or the name of a function and cannot be used as a variable name.')
                                    sys.exit(-1)
                            exec(__command)
                            for variable in variables:    
                                print(f'{__lcv}: {__command} ==> {variable} == {eval(variable)}')
                        else:
                            exec(__command)
                            print(f'{__lcv}: {__command}')
                        __lcv += 1
                    except Exception as e:
                        print(f'ERROR on line {__lcv+1}: {__command}\n ==> {e}')
                        sys.exit(-1)

            __lcv += 1    

        # if a line is not a python block, check to see if it contains any
        #  python commands to insert through @ ... @   
        elif hasPython(__data[__lcv]):
            while hasPython(__data[__lcv]):
                __snippet = getPython(__data[__lcv])
                try:
                    __result = eval(__snippet)
                    __data[__lcv] = strsub(__snippet, __result, __data[__lcv])
                except Exception as e:
                    print(f'ERROR on line {__lcv+1}: {__data[__lcv]}\n ==> {e}')
                    sys.exit(-1)

        else:
            __lcv += 1

    __data = removeVariableDeclarations(__data)

    return __data

if __name__ == '__main__':
    main()