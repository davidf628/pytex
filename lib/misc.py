import re, os, sys
from random import choice, choices, sample

def test():
    test_getFunctionAndArgs()

def hasPython(s):
    return re.search(r'\@.*\@', s) != None

def getPython(s):
    return re.search(r'\@(.*?)\@', s).group(1)

def getPythonWithEyes(s):
    return re.search(r'(\@.*?\@)', s).group(1)

def uncommentLine(s, remove_initial_whitespace=True):
    if re.search(r'^\s*\%\s*', s):
        if remove_initial_whitespace:
            return re.search(r'^\s*\%\s*(.*)', s).group(1)
        else:
            return re.search(r'^\s*\%(\s*.*)', s).group(1)
    else:
        return s

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True

def getCommand(line):
    line = line.replace('%','').replace('{', '').replace('}','')
    line = line.split('where')[0].strip()
    return line

def strsub(target, value, s):
    if is_number(value):
        return re.sub(f'\\@.*?\\@', str(value), s, 1)
    else:
        return s.replace(f'@{target}@', value)

def removeVariableDeclarations(data):
    i = 0
    while i < len(data):
        if isNewPythonCommands(data[i]):
            while not isEndPythonCommands(data[i]):
                data.pop(i)
            data.pop(i)
        else:
            i += 1

    return data

def hasVariableCall(s):
    return re.search(r'\@[A-Za-z_]\w*\@', s) != None

def getVariableName(s):
    return re.search(r'\@([A-Za-z_]\w*)\@', s).group(1)

def replaceVar(expr, var, val):
    return re.sub(f'@{var}@', str(val), expr)


def hasArrayCall(s):
    return re.search(r'\@([A-Za-z_]\w*)\[([0-9]*|\@[A-Za-z_]\w*\@)\]\@', s) != None

def getArrayAndIndex(s):
    result = re.search(r'\@([A-Za-z_]\w*)\[([0-9]*|\@[A-Za-z_]\w*\@)\]\@', s)
    return [ result.group(1), result.group(2) ]

def subvars(expr, vars):
    while hasVariableCall(expr):
        var_name = getVariableName(expr)
        if var_name in vars:
            expr = replaceVar(expr, var_name, vars[var_name])
    while hasArrayCall(expr) or hasVariableCall(expr):
        if hasVariableCall(expr):
            pass
        elif hasArrayCall(expr):
            var_name, index = getArrayAndIndex(expr)
            if var_name in vars:
                pass

    return expr

# Returns true if 's' begins with the word: %variables
def isNewPythonCommands(s):
    return re.search(r'^\s*\%\s*python\s*$', s, re.IGNORECASE) != None

def isEndPythonCommands(s):
    return re.search(r'^\s*\%\s*end\s*$', s, re.IGNORECASE) != None

def setVersionValue(data, version):
    i = 0
    done = False
    while i < len(data) and not done:
        if re.search(r'\\newcommand{\\version}{.*}', data[i]) != None:
            data[i] = '\\newcommand{\\version}{' + version + '}'
            done = True
        i += 1
    return data
            

def setKeyFlag(data, iskey):
    i = 0
    done = False
    while i < len(data) and not done:
        if re.search(r'\\setboolean{make_key}{.*}', data[i]) != None:
            data[i] = '\\setboolean{make_key}{' + str(iskey).lower() + '}'
            done = True
        i += 1
    return data

import re

def getFunctionAndArgs(line):
    # Define the regex pattern to match function definitions
    pattern = r'([a-zA-Z_]\w*)\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)'
    # Search for the pattern in the line
    match = re.search(pattern, line)
    
    if match:
        # Extract function name
        function_name = match.group(1)
        # Extract function arguments
        args = match.group(2).split(',') if match.group(2) else []
        args = [arg.strip() for arg in args]  # Trim whitespace
        
        return function_name, args
    else:
        return None, None

def test_getFunctionAndArgs():
    line = "my_function('afile.tex', 'bfile.tex', prefixcode='\item (2 pts)')"
    function_name, args = getFunctionAndArgs(line)
    print("Function Name:", function_name)
    print("Arguments:", args)

def load_pytex_file(filename):
    data = []
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            for line in f:
                data.append(line)
    else:
        print(f'ERROR: file {filename} not found.')
        sys.exit(-1)
    return data

def checkImportStatements(data):

    newData = []

    inPythonCommands = False

    i = 0
    while i < len(data):

        if isNewPythonCommands(data[i]):
            inPythonCommands = True        

        if isEndPythonCommands(data[i]):
            inPythonCommands = False

        if 'importpytex' in data[i] or 'importrandpytexfrom' in data[i]:

            if inPythonCommands:
                print(f'\n-- Error on Line: {i+1} --\n')
                print('SORRY! You aren\'t permitted to import a pytex file into a \%python ... \%end statement block.')
                print('  You must use a @ ... @ statement on a single line instead.\n')
                quit()
                
            elif hasPython(data[i]):
                snippet = getPython(data[i])
                function_name, argument_list = getFunctionAndArgs(snippet)

                if function_name == 'importpytex':
                    
                    # remove the importpytex statement
                    data[i] = data[i].replace(getPythonWithEyes(data[i]), '')
                    
                    # add the rest of the line to the return buffer
                    newData.append(data[i])
                    
                    # parse the arguments supplied to importpytex
                    choose = 1
                    withreplacement = False
                    prefixcode = ''
                    files_to_pick_from = []
                    files_to_import = []
                    for arg in argument_list:
                        if arg.lower().startswith('withreplacement'):
                            _, value = arg.split('=')
                            withreplacement = value.lower() == 'True'.lower() 
                        elif arg.lower().startswith('choose'):
                            _, value = arg.split('=')
                            choose = int(value)
                        elif arg.lower().startswith('prefixcode'):
                            _, value = arg.split('=')
                            prefixcode = remove_quote_marks(value)
                        else:
                            files_to_pick_from.append(remove_quote_marks(arg))

                    # choose the pytex files to import
                    if withreplacement:
                        files_to_import = choices(files_to_pick_from, k=choose)
                    else:
                        files_to_import = sample(files_to_pick_from, k=choose)

                    for filename in files_to_import:
                        newData = [*newData, prefixcode, *load_pytex_file(filename)]
                    i += 1 
        else:
            newData.append(data[i])
            i += 1

    return newData

def is_function_statement(line):
    function_pattern = r'^\s*\w*\(.*\)'
    return bool(re.search(function_pattern, line))

def remove_quote_marks(s):
    s = s.strip()
    if s[0] == '"' or s[0] == '\'':
        s = s[1:]
    if s[-1] == '"' or s[-1] == '\'':
        s = s[:-1]
    return s


###############################################################################
# Determines the amount of initial whitespace present for a command. Used to
#  figure out when a code block begins and ends

def get_indentation_amount(command):
    # bypass the initial '%' comment marker and any whitespace before it
    command = re.search(r'^(\s*%)?(.*)', command).group(2)

    counter = 0
    while counter < len(command) and (command[counter] == ' ' or command[counter] == '\t'):
        counter += 1
    return counter


###############################################################################
# Checks to see if a command is the start of a python code block such as:
#   while i < len(data):
# It just checks for the semicolon at the end of the statement

def is_python_code_block(command):
    # looks for a statement of the form: "while x > 10:"
    pattern = r'.*:\s*$'
    return bool(re.search(pattern, command))
    

###############################################################################
# Goes through python code and selects sequential lines that are indented,
#  indicating a continued block of code that needs to be executed as a group
# 
#  Returns the code block as a string, ready to be sent to exec()

def get_python_code_block(data, current_line):
    
    # get initial statement that begins the code block
    command = uncommentLine(data[current_line], remove_initial_whitespace=False)
    block_length = 1
    base_indentation = get_indentation_amount(command)
    command = command[base_indentation:] # skip any spaces the user put in for formatting
    code_block = command
    
    # move forward to the next statement, which should be in the code block
    current_line += 1
    command = uncommentLine(data[current_line], remove_initial_whitespace=False)
    command = command[base_indentation:]
    
    while current_line < len(data) and (get_indentation_amount(command) > base_indentation or is_else_or_elif(command, base_indentation)):
        code_block += f'\n{command}'
        current_line += 1
        command = uncommentLine(data[current_line], remove_initial_whitespace=False)
        block_length += 1
        command = command[base_indentation:]
        
    return (code_block, block_length)

###############################################################################
# Skips all initial spaces and LaTeX comment symbol, and then any additional
#  spaces and retrieves the first 'word' that exists in a command. Used to 
#  find any uses of 'else' or 'elif' because you can't tell that an 'if' 
#  statement block has ended just by spaces alone

def is_else_or_elif (command, base_indentation):
    indentation_amount = get_indentation_amount(command)
    if indentation_amount == base_indentation:
        pattern = r'^\s*%\s*(else|elif):?\s*'
        return re.search(pattern, command) != None
    else:
        return False

###############################################################################
## Checks to see if a string qualifies as a valid variable name

def is_valid_variable_name (s):
    return re.search(r'(?<!\.)\s*\b([a-zA-Z_]\w*)(?:\[[0-9a-zA-Z_\*\\\+\-\s]*\])?\s*', s) != None

def extract_variable_names(code):

    # remove any comments that may exist in the line
    if code.find('#') != -1:
        code = code[:code.find("#")]

    variable_names = []
    variable_pattern = r'(?<!\.)\b([a-zA-Z_]\w*(?:\[[0-9a-zA-Z_\*\\\+\-\s]*\])?)\s*=\s*\.*'
    possible_variable = bool(re.search(variable_pattern, code))
    is_assignment_statement = possible_variable and not is_function_statement(code)

    if is_assignment_statement:
        variables = code.split('=')[0]
        variable_names = variables.split(',')
        for i in range(0, len(variable_names)):
            if is_valid_variable_name(variable_names[i]):
                variable_names[i] = re.match(r'(?<!\.)\s*\b([a-zA-Z_]\w*)(?:\[[0-9a-zA-Z_\*\\\+\-\s]*\])?\s*', variable_names[i]).group(1)
            else:
                variable_names[i] = ''
    
    return variable_names

def test_extract_variable_names():
    code1 = "x = 5"
    code2 = "y = x + 3"
    code3 = "z = 'hello'"
    code4 = "arr = [1, 2, 3]"
    code5 = "a, b, c = 1, 2, 3"
    code6 = "d, e, f = some_function()"
    code7 = "arr[0] = 10"
    code8 = "arr[1] = y"
    code9 = "arr[2] = arr[0] + arr[1]"
    code10 = "m = rand(25, 36)"
    code11 = "avg = mean([a, b, c])"
    code12 = "sol = 'a. Reject $H_0$' if (p <= a) else 'b. Fail to reject $H_0$'"
    code13 = r"print(f'a == {a}')"
    code14 = 'balance.append(rand(1000, 2000, prec=10))'

    print(extract_variable_names(code1))  # Output: ['x']
    print(extract_variable_names(code2))  # Output: ['y']
    print(extract_variable_names(code3))  # Output: ['z']
    print(extract_variable_names(code4))  # Output: ['arr']
    print(extract_variable_names(code5))  # Output: ['a', 'b', 'c']
    print(extract_variable_names(code6))  # Output: ['d', 'e', 'f']
    print(extract_variable_names(code7))  # Output: ['arr']
    print(extract_variable_names(code8))  # Output: ['arr']
    print(extract_variable_names(code9))  # Output: ['arr']
    print(extract_variable_names(code10))  # Output: ['m']
    print(extract_variable_names(code11))  # Output: ['avg']
    print(extract_variable_names(code12))  # Output: ['sol']
    print(extract_variable_names(code13))  # Output: ['']
    print(extract_variable_names(code14))  # Output: ['balance']

def command_contains_reserved_word(command):
    variables = extract_variable_names(command)
    for variable in variables:
        if variable in __internal_declarations:
            return variable
    return False

__internal_declarations = [
    # internal global variables from pytex.py
    '__lcv', '__internal_declarations', '__data', '__line', '__stack', 
    '__rptcounter', '__blockstart', '__command', '__snippet', '__result',
    '__f', '__version', '__parseinfo',
    # python keywords
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
    'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally',
    'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
    'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
    # python built-in functions
    'abs', 'aiter', 'all', 'anext', 'any', 'ascii', 'bin', 'bool', 'breakpoint',
    'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex',
    'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter',
    'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash',
    'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter',
    'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object',
    'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed',
    'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum',
    'super', 'tuple', 'type', 'vars', 'zip', '__import__',
    # functions in the python 'math' library
    'ceil', 'comb', 'copysign', 'fabs', 'factorial', 'floor', 'fmod', 'frexp',
    'fsum', 'gcd', 'isclose', 'isfinite', 'isinf', 'isnan', 'isqrt', 'lcm',
    'ldexp', 'modf', 'nextafter', 'perm', 'prod', 'remainder', 'sumprod',
    'trunc', 'ulp', 'cbrt', 'exp', 'exp2', 'expm1', 'log', 'log1p', 'log2',
    'log10', 'pow', 'sqrt', 'acos', 'asin', 'atan', 'atan2', 'cos', 'dist',
    'hypot', 'sin', 'tan', 'degrees', 'radians', 'acosh', 'asinh', 'atanh',
    'cosh', 'sinh', 'tanh', 'erf', 'erfc', 'gamma', 'lgamma', 'pi', 'e', 'tau',
    'inf', 'nan', 
    # functions in the python 'sympy' libary declared globally
    'symbols', 'latex', 'factor', 'expand', 'solve', 'simplify', 'Eq', 'Rational',
    # functions in arrays.py
    'calconarray', 'sorta', 'sortd', 'joinarray', 'latexjoinarray',
    # functions in display.py
    'showdataarray', 'horizshowarrays', 'showarrays', 'normalcurve', 'tcurve',
    'dotplot', 'boxandwhiskerplot',
    # functions in maths.py
    'sign', 'sgn', 'frac', 'reducefraction', 'evalfunc', 'rnd', 'towords'
    # functions in misc.py
    'hasPython', 'getPython', 'uncommentLine', 'is_number', 'getCommand',
    'strsub', 'removeVariableDeclarations', 'hasVariableCall', 'getVariableName',
    'replaceVar', 'hasArrayCall', 'getArrayAndIndex', 'subvars',
    'isNewPythonCommands', 'isEndPythonCommands', 'extract_variable_names',
    'command_contains_reserved_word', 'importpytex', 'importpytexfrom',
    'checkImportStatements', 'getFunctionAndArgs', 'is_function_statement',
    'load_pytex_file', 'getPythonWithEyes', 'remove_quote_marks', 
    'is_python_code_block', 'get_python_code_block', 'get_indentation_amount',
    'is_valid_variable_name',
    # functions in randomizers.py
    'seed', 'rand', '__randval', 'rands', 'diffrands', 'nzrand', 'nzrands', 
    'nzdiffrands', 'randfrom', 'randsfrom', 'diffrandsfrom', 'singleshuffle', 
    'jointshuffle', 'multiplechoiceshuffle', 'randsgn', 
    # functions in stats.py
    'normalcdf', 'invnorm', 'tcdf', 'invt', 'binompdf', 'binomcdf', 'binommean',
    'binomstdev', 'mean', 'weightedsort', 'median', 'modes', 'stdevp', 'stdev',
    'linreg', 'classranges', 'getclasslimits', 'frequencies', 'midpoints',
    'relativefreq', 'cumulativefreq', 'quartiles',
     # import functions
     'importpytex', 'importrandpytexfrom' ]

if __name__ == '__main__':
    test()