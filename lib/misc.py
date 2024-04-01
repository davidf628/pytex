import re

def test():
    print(getCommand('% a = rand(2, 5) where a > b'))

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

if __name__ == '__main__':
    test()