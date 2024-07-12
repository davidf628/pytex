import os, random, sys

def parseCommandLine(args, version):

    parseInfo = {}

    # The following part of this function does the command line parsing

    # if no command line args are passed, then display help
    if len(args) == 1:
        args.append('-h')

    for arg in args[1:]:

        # remove all leading dashes for new commands
        while arg[0] == '-':
            arg = arg[1:]

        if '=' in arg:
            command, value = arg.split('=')
            command = command.strip().lower()
            value = value.strip()
        else:
            command = arg.strip()

        if command.lower() == 'h' or command.lower() == 'help':

            print(f'\nPyTeX Copyright David Flenner version: {version}\n')
            print(f'Command Line: pytex [--args] "filename.tex"\n')
            print(f' --h, or --help         :  Displays this menu\n')
            print(f' --s=#, or --seed=#     :  Uses the random seed indicated by the value at #, which should ')
            print(f'                              be an integer, but can be a string (with no spaces) as well.\n')
            print(f' --v=*, or --version=*  :  Defines a version value for your exam such as A, B, etc.\n')
            print(f' --k, or key            :  This flag tells PyTeX to generate a key for the current ')
            print(f'                              document. For this functionality to work, PyTeX assumes that')
            print(f'                              you have declared a boolean variable "make_key" that it can')
            print( '                              adjust the value through the line: \setboolean{make_key}{false}.')
            print( '                              See the PyTeX documentation for more detailed information.\n')
            print(f' --o=*, or --output=*   :  The name of the output file to create. The default is to append')
            print(f'                              "out_" to the original filename. If spaces are to be used,')
            print(f'                              then double quotes are required around the file name.\n')

            sys.exit(0)

        elif command.lower() == 's' or command.lower() == 'seed':
            parseInfo['seed'] = value
        
        elif command.lower() == 'v' or command.lower() == 'version':
            parseInfo['version'] = value

        elif command.lower() == 'k' or command.lower() == 'key':
            parseInfo['key'] = True

        elif command.lower() == 'o' or command.lower() == 'output':
            value = value[1:] if value[0] == '"' else value
            value = value[:-1] if value[-1] == '"' else value
            parseInfo['outputfilename'] = value

        else:
            command = command[1:] if command[0] == '"' else command
            command = command[:-1] if command[-1] == '"' else command
            parseInfo['filename'] = command

    # The second part sets up all the different file names that need to be tracked
    if 'filename' in parseInfo.keys(): 

        if os.path.isfile(parseInfo['filename']):
            parseInfo['filepath'] = os.path.dirname(parseInfo['filename'])
            parseInfo['relfilename'] = os.path.basename(parseInfo['filename'])
            parseInfo['basefilename'], parseInfo['extension'] = os.path.splitext(parseInfo['relfilename'])
            if not 'outputfilename' in parseInfo.keys():
                if 'version' in parseInfo.keys():
                    if 'key' in parseInfo.keys():
                        parseInfo['outputfilename'] = f'{parseInfo["basefilename"]} {parseInfo["version"]} Key{parseInfo["extension"]}'
                    else:
                        parseInfo['outputfilename'] = f'{parseInfo["basefilename"]} {parseInfo["version"]}{parseInfo["extension"]}'
                else:
                    parseInfo['outputfilename'] = f'out_{parseInfo["relfilename"]}'
            parseInfo['baseoutputname'], _ = os.path.splitext(parseInfo['outputfilename'])
            parseInfo['baseoutputname'] = os.path.join(parseInfo['filepath'], parseInfo['baseoutputname'])
            parseInfo['outputfile'] = f'{parseInfo["baseoutputname"]}.tex'
            parseInfo['aux'] = f'{parseInfo["baseoutputname"]}.aux'
            parseInfo['log'] = f'{parseInfo["baseoutputname"]}.log'
            parseInfo['gz'] = f'{parseInfo["baseoutputname"]}.synctex.gz' 

        else:
            print(f'File: {parseInfo["filename"]} not found ==> exiting')
            sys.exit(-1)

    # The third part ensures that a random seed is created
    if not 'seed' in parseInfo.keys():
        parseInfo['seed'] = round(random.random() * 100000000000)

    if not 'key' in parseInfo.keys():
        parseInfo['key'] = False

    if not 'version' in parseInfo.keys():
        parseInfo['version'] = ''

    return parseInfo


def patchArgs(args):

    i = 0
    newargs = []

    while i < len(args):
        arg = args[i].strip()

        if arg[0] == '"' and arg[-1] != '"':
            newarg = ""
            while arg[-1] != '"' and i < len(args):
                arg = args[i].strip()
                newarg += f'{arg} '
                i += 1
            newargs.append(newarg)
        else:
            newargs.append(arg)            
        i += 1

    return newargs

