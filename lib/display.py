from numpy import transpose
from lib import *
import math

def display_test():
    boxandwhiskerplot([15, 19, 25, 25, 26, 34, 32, 33, 35, 37, 39, 40, 45, 48, 49, 51, 80])

def showdataarray(array, columns=1, options=""):
    alignment = "|"
    strarray = []
    for _ in range(0, columns):
        alignment += "c|"

    tablecode = '\\begin{tabular}' + '{' + alignment + '}\n  \\hline\n' 
    
    for i in range(0, len(array)):
        strarray.append(str(array[i]))

    while len(strarray) % columns != 0:
        strarray.append('')

    for i in range(0, len(strarray), columns): 
        row = ' & '.join(strarray[i:i+columns])
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


def normalcurve(leftbound, rightbound, mean=0, stdev=1, twotail=False):
    
    funcstr = r"normal(\x,\m,\s) = 1 / (\s * sqrt(2 * pi)) * exp(-(\x-\m)^2/(2*\s^2));"
    func = f'normal(x, {mean}, {stdev})'
    lowerlimit = -4 * stdev + mean
    upperlimit = 4 * stdev + mean

    labels = ''
    if leftbound < lowerlimit:
        leftbound = lowerlimit
    else:
        labels += f'{leftbound}'
    
    if rightbound > upperlimit:
        rightbound = upperlimit
    else:
        if len(labels) == 0:
            labels += f'{rightbound}'
        else:
            labels += f',{rightbound}'

    plotstr = r"\begin{tikzpicture}[ declare function = {" +funcstr+ r"} ]" + "\n"
    plotstr += r"   \begin{axis}[" + "\n"
    plotstr += r"      no markers, domain=-4:4, samples=100," + "\n"
    plotstr += r"      axis lines*=left, xlabel=$x$, ylabel=$y$," + "\n"
    plotstr += r"      every axis y label/.style={at=(current axis.above origin),anchor=south}," + "\n"
    plotstr += r"      every axis x label/.style={at=(current axis.right of origin),anchor=west}," + "\n"
    plotstr += r"      height=5cm, width=12cm," + "\n"
    plotstr += r"      xtick={" + labels + r"}, ytick=\empty," + "\n"
    plotstr += r"      enlargelimits=false, clip=false, axis on top," + "\n"
    plotstr += r"      grid = major ]" + "\n"
    if twotail:
        domain = f'{lowerlimit}:{leftbound}'
        plotstr += r"      \addplot [fill=cyan!20, draw=none, domain=" + domain + r"] {" + func + r"} \closedcycle;" + "\n"
        domain = f'{rightbound}:{upperlimit}'
        plotstr += r"      \addplot [fill=cyan!20, draw=none, domain=" + domain + r"] {" + func + r"} \closedcycle;" + "\n"
    else:
        domain = f'{leftbound}:{rightbound}'
        plotstr += r"      \addplot [fill=cyan!20, draw=none, domain=" + domain + r"] {" + func + r"} \closedcycle;" + "\n"
    plotstr += r"      \addplot [very thick,cyan!50!black] {" + func + r"};" + "\n"
    plotstr += r"    \end{axis}" + "\n"
    plotstr += r"\end{tikzpicture}" + "\n"

    return plotstr

def tcurve(leftbound, rightbound, df, mean=0, stdev=1, twotail=False):

    numerator = math.gamma( (df + 1) / 2)
    denominator = math.sqrt( math.pi * df) * math.gamma ( df / 2 )
    factor = numerator / denominator
   
    funcstr = r"tpdf(\t,\df) = " + str(factor) + r" * (1 + (\t)^2 / \df)^ ( -(\df + 1) / 2 );"
    func = f'tpdf(x, {df})'
    lowerlimit = -4 * stdev + mean
    upperlimit = 4 * stdev + mean

    labels = ''
    if leftbound < lowerlimit:
        leftbound = lowerlimit
    else:
        labels += f'{leftbound}'
    
    if rightbound > upperlimit:
        rightbound = upperlimit
    else:
        if len(labels) == 0:
            labels = f'{rightbound}'
        else:
            labels += f',{rightbound}'

    plotstr = r"\begin{tikzpicture}[ declare function = {" +funcstr+ r"} ]" + "\n"
    plotstr += r"   \begin{axis}[" + "\n"
    plotstr += r"      no markers, domain=-4:4, samples=100," + "\n"
    plotstr += r"      axis lines*=left, xlabel=$x$, ylabel=$y$," + "\n"
    plotstr += r"      every axis y label/.style={at=(current axis.above origin),anchor=south}," + "\n"
    plotstr += r"      every axis x label/.style={at=(current axis.right of origin),anchor=west}," + "\n"
    plotstr += r"      height=5cm, width=12cm," + "\n"
    plotstr += r"      xtick={" + labels + r"}, ytick=\empty," + "\n"
    plotstr += r"      enlargelimits=false, clip=false, axis on top," + "\n"
    plotstr += r"      grid = major ]" + "\n"
    if twotail:
        domain = f'{lowerlimit}:{leftbound}'
        plotstr += r"      \addplot [fill=cyan!20, draw=none, domain=" + domain + r"] {" + func + r"} \closedcycle;" + "\n"
        domain = f'{rightbound}:{upperlimit}'
        plotstr += r"      \addplot [fill=cyan!20, draw=none, domain=" + domain + r"] {" + func + r"} \closedcycle;" + "\n"
    else:
        domain = f'{leftbound}:{rightbound}'
        plotstr += r"      \addplot [fill=cyan!20, draw=none, domain=" + domain + r"] {" + func + r"} \closedcycle;" + "\n"
    plotstr += r"      \addplot [very thick,cyan!50!black] {" + func + r"};" + "\n"
    plotstr += r"    \end{axis}" + "\n"
    plotstr += r"\end{tikzpicture}" + "\n"

    return plotstr

###############################################################################
# Draws a basic dot plot from statistics from a single set of data that is 
#  assummed to be integer based
#  
#  The available options are:
#   - xdist: the physical distance between x-tick marks (5mm, 6pt, etc)
#   - ydist: the physical distance between each y-tick mark
#   - xmin: the smallest value to use along the x-axis
#   - xmax: the largest value to use along the x-axis
#   - xscl: the distance between tick marks

def dotplot(data, xdist=None, ydist="5mm", xmin=None, xmax=None, xscl=None):

    counts = {}
    maxcount = 0
    # get the count of each data item in the data set
    for val in data:
        if counts.get(val, None) == None:
            counts[val] = 1
        else:
            counts[val] += 1
        if counts[val] > maxcount:
            maxcount = counts[val]

    # sort the counts and get the minimum and maximum values
    counts = dict(sorted(counts.items()))
    
    if xmin == None:
        xmin = list(counts.keys())[0]
    if xmax == None:
        xmax = list(counts.keys())[-1]

    coordinates = ""
    for xval in counts.keys():
        for yval in range(1, counts[xval]+1):
            coordinates += f"({xval},{yval}) "

    plotstr = r"\begin{tikzpicture}" + "\n"
    plotstr += r"  \begin{axis}[axis lines=center, axis y line=none," + "\n"
    if xdist == None:
        plotstr += f"     y={ydist},"
    else:
        plotstr += f"     x={xdist}, y={ydist},"
    if xscl != None:
        plotstr += f" xtick distance={xscl},\n"
    plotstr += r"     axis line style={stealth-stealth, thick}," + "\n"
    plotstr += f"     xmin={xmin}, xmax={xmax}, ymin=0, ymax={maxcount}]" + "\n"
    plotstr += r"     \addplot [only marks, color=black, thick] coordinates { " + coordinates + r" };" + "\n"
    plotstr += r"  \end{axis}" + "\n"
    plotstr += r"\end{tikzpicture}" + "\n"

    return plotstr


###############################################################################
# Draws a basic box and whisker plot from statistics for a single data set 
#  
#  The available options are:
#   - fromquartiles: whether or not the data represents quartiles or a set of
#       data values
#   - xdist: the physical distance between x-tick marks (5mm, 6pt, etc)
#   - ydist: the physical distance between each y-tick mark
#   - xmin: the smallest value to use along the x-axis
#   - xmax: the largest value to use along the x-axis
#   - xscl: the distance between tick marks

def boxandwhiskerplot(data, fromquartiles=False, xdist=None, ydist="5mm", xmin=None, xmax=None, xscl=None):

    if fromquartiles:
        q = { 'min': data[0], 'q1': data[1], 'med': data[2], 'q3': data[3], 'max': data[4] }
    else:
        q = quartiles(data)
    
    if xmin == None:
        xmin = q['min']
    if xmax == None:
        xmax = q['max']

    plotstr = r"\begin{tikzpicture}" + "\n"
    plotstr += r"  \begin{axis}[axis lines=center, axis y line=none," + "\n"
    if xdist == None:
        plotstr += f"    y={ydist},"
    else:
        plotstr += f"    x={xdist}, y={ydist},"
    if xscl != None:
        plotstr += f" xtick distance={xscl},\n"
    else:
        plotstr += "\n"
    plotstr += r"    axis line style={stealth-stealth, thick}," + "\n"
    plotstr += f"    xmin={xmin}, xmax={xmax}, ymin=0, ymax=2]" + "\n"
    plotstr += f"    \\draw [thick, black] (axis cs:{q['min']},0.6) -- (axis cs:{q['min']},1.4); \n"
    plotstr += f"    \\draw [thick, black] (axis cs:{q['q1']},0.5) -- (axis cs:{q['q1']},1.5); \n"
    plotstr += f"    \\draw [thick, black] (axis cs:{q['med']},0.5) -- (axis cs:{q['med']},1.5); \n"
    plotstr += f"    \\draw [thick, black] (axis cs:{q['q3']},0.5) -- (axis cs:{q['q3']},1.5); \n"
    plotstr += f"    \\draw [thick, black] (axis cs:{q['max']},0.6) -- (axis cs:{q['max']},1.4); \n" 
    plotstr += f"    \\draw [thick, black] (axis cs:{q['min']},1.0) -- (axis cs:{q['q1']},1.0); \n"
    plotstr += f"    \\draw [thick, black] (axis cs:{q['q3']},1.0) -- (axis cs:{q['max']},1.0); \n"
    plotstr += f"    \\draw [thick, black] (axis cs:{q['q1']},1.5) -- (axis cs:{q['q3']},1.5); \n"
    plotstr += f"    \\draw [thick, black] (axis cs:{q['q1']},0.5) -- (axis cs:{q['q3']},0.5); \n"
    plotstr += r"  \end{axis}" + "\n"
    plotstr += r"\end{tikzpicture}" + "\n"

    print(plotstr)

    return plotstr

if __name__ == '__main__':
    display_test()