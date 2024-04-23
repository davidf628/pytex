
def parseCommandLine(args, version):

    parseInfo = {}

    for arg in args[1:]:

        # remove all leading dashes for new commands
        while arg[0] == '-':
            arg = arg[1:]

        if '=' in arg:
            command, value = arg.split('=')
            command = command.strip().lower()
            value = value.strip().lower()
        else:
            command = arg.strip().lower()

        if command == 'v' or command == 'version':
            print(f'PyTeX Copyright David Flenner version: {version}')

        elif command == 'h' or command == 'help':
            print(f'\nPyTeX Copyright David Flenner version: {version}\n')
            print(f'Command Line: pytex [--args] "filename.tex"')
            print(f' --h, or --help         :  Displays this menu')
            print(f' --v, or --version      :  Dislpays version information')
            print(f' --s=#, or --seed=#     :  Uses the random seed indicated by the value at #, which should ')
            print(f'                              be an integer, but can be a string (with no spaces) as well.')
            print(f' --v=*, or --version=*  :  Defines a version value for your exam such as A, B, etc.')
            print(f' --key=[true or false]  :  The default behaviour is key=false, which will tell PyTeX to ')
            print(f'                              not generate a key for the current document. For this')
            print(f'                              functionality to work, PyTeX assumes that you have declared')
            print(f'                              a boolean variable "make_key" that it can adjust the value')
            print( '                              through the line: \setboolean{make_key}{false}. See the ')
            print(f'                              documentation for more detailed information.')
            print(f' --o=*, or --output=*   :  The name of the output file to create. The default is to append')
            print(f'                              "out_" to the original filename. If spaces are to be used,')
            print(f'                              then double quotes are required around the file name.')

        elif command == 's' or command == 'seed':
            parseInfo['seed'] = value
        
        elif command == 'v' or command == 'version':
            parseInfo['version'] = value

        elif command == 'key':
            if value == 'f' or value == 'false':
                parseInfo['key'] = False
            elif value == 't' or value == 'true':
                parseInfo['key'] = True
            else:
                parseInfo['key'] = False

        elif command == 'o' or command == 'output':
            parseInfo['outputfilename'] = value

        else:
            parseInfo['filename'] = command

    return parseInfo