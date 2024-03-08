import sys, re, random

sys.argv.append('test.tex')

def rand(low, high):
    return random.randint(low, high)

# Read the .tex file specified from the command line and load it

filename = sys.argv[1]
data = []

with open(filename, "r") as f:
    for line in f:
        data.append(line)

eod = 0 # End of TeX document, i.e. the line where \end{document} occurs
# skip over all lines until the end of the TeX document
for line_no, line in enumerate(data):
    if re.search(r'\\end\s*\{document\}', line):
        eod = line_no
        print(f'Line Number: {line_no}')

print(eval('2+2'))

# start reading in the different variables and begin the randomization
vars = {}
for i in range(eod+1, len(data)):
    if data[i].strip() != '': # skip empty lines
        result = re.search(r'([A-Za-z_]\w*)\s*=\s*(.*)', data[i])
        if result:
            vars[result.group(1)] = eval(result.group(2)) # save a record of the variable
            exec(f'{result.group(1)} = {vars[result.group(1)]}') # put the variable and its value into memory
            print(vars)

# replace all the locations of the variables within the TeX document

for i in range(0, eod):
    result = re.search(r'@\s*([A-Za-z_]\w*)\s*@', data[i])
    if result:
        variable_name = result.group(1)
        print(f'newval == {vars[variable_name]}')
        data[i] = re.sub(r'@\s*([A-Za-z_]\w*)\s*@', str(vars[variable_name]), data[i])
        print(data[i])



