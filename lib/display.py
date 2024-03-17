from numpy import transpose

def display_test():
    print(showarrays('data', [1, 2, 3, 4, 5, 6], 'more data', [7, 8, 9, 91, 22]))

def showdataarray(array, columns=1, options=""):
    alignment = "|"
    for _ in range(0, columns):
        alignment += "c|"

    tablecode = '\\begin{tabular}' + '{' + alignment + '}\n  \\hline\n' 
    
    for i in range(0, len(array)):
        array[i] = str(array[i])

    while len(array) % columns != 0:
        array.append('')

    for i in range(0, len(array), columns): 
        row = ' & '.join(array[i:i+columns])
        tablecode += '  ' + row + ' \\\\\n  \\hline\n'

    tablecode += '\\end{tabular}\n'
        
    return tablecode

def horizshowarrays(*args):
    title = ""
    width = 0
    data = []

    # combind the string titles and data into one large array
    for arg in args:
        if type(arg) == str:
            title = '\\textbf{' + str(arg) +'}'
        elif type(arg) == list:
            newlist = arg.copy()
            newlist.insert(0, title)
            width = max(len(newlist), width)
            data.append(newlist)

    # create a table for that array
    alignment = "|l|"
    for _ in range(0, width-1):
        alignment += "c|"

    tablecode = '\\begin{tabular}' + '{' + alignment + '}\n  \\hline\n' 
    
    for row in range(0, len(data)):
        for col in range(0, len(data[row])):
            data[row][col] = str(data[row][col])

    for row in data:
        while len(row) < width:
            row.append('')
        line = ' & '.join(row)
        tablecode += '  ' + line + ' \\\\\n  \\hline\n'

    tablecode += '\\end{tabular}\n'
        
    return tablecode

def showarrays(*args):
    title = ""
    width = 0
    data = []
    nlists = 0

    # combind the string titles and data into one large array
    for arg in args:
        if type(arg) == str:
            title = '\\textbf{' + str(arg) +'}'
        elif type(arg) == list:
            newlist = arg.copy()
            newlist.insert(0, title)
            width = max(len(newlist), width)
            data.append(newlist)
            nlists += 1

    # make sure all rows are the same length
    for row in data:
        while len(row) < width:
            row.append('')

    # make sure all data in the arrays are represented as strings
    for row in range(0, len(data)):
        for col in range(0, len(data[row])):
            data[row][col] = str(data[row][col])

    data = transpose(data)

    # create a table for that array
    alignment = "|c|"
    for _ in range(1, nlists):
        alignment += "c|"

    tablecode = '\\begin{tabular}' + '{' + alignment + '}\n  \\hline\n' 

    for row in data:

        line = ' & '.join(row)
        tablecode += '  ' + line + ' \\\\\n  \\hline\n'

    tablecode += '\\end{tabular}\n'
        
    return tablecode


if __name__ == '__main__':
    display_test()