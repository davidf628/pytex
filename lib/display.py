def display_test():
    print(showdataarray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 15))

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

if __name__ == '__main__':
    display_test()