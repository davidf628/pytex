import re

def test():
    test_extract_variable_names()

def hasPython(s):
    return re.search(r'\@.*\@', s) != None

def getPython(s):
    return re.search(r'\@(.*?)\@', s).group(1)

def uncommentLine(s):
    if re.search(r'^\s*\%\s*', s):
        return re.search(r'^\s*\%\s*(.*)', s).group(1)
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

def extract_variable_names(code):
    variable_names = []
    pattern = r'(?<!\.)\b([a-zA-Z_]\w*(?:\[[0-9a-zA-Z_\*\\\+\-\s]*\])?)\s*=\s*\.*'
    is_assignment_statement = bool(re.search(pattern, code))

    if is_assignment_statement:
        variables = code.split('=')[0]
        variable_names = variables.split(',')
        for i in range(0, len(variable_names)):
            variable_names[i] = re.match(r'(?<!\.)\s*\b([a-zA-Z_]\w*)(?:\[[0-9a-zA-Z_\*\\\+\-\s]*\])?\s*', variable_names[i]).group(1)
    
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

def command_contains_reserved_word(command):
    variables = extract_variable_names(command)
    for variable in variables:
        if variable in internal_declarations:
            return variable
    return False

internal_declarations = ['normalcdf', 'invnorm', 'tcdf', 'invt', 'mean']

if __name__ == '__main__':
    test()