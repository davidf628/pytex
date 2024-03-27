from scipy.stats import norm, t, binom, linregress
import numpy as np
import math

def stats_test():
    classes = classranges(6, minval=7, class_width=9)
    print(classes)

def normalcdf (lower, upper, mean=0, stdev=1):
    return norm.cdf(upper, mean, stdev) - norm.cdf(lower, mean, stdev)

def invnorm (p, mean=0, stdev=1):
    return norm.ppf(p, mean, stdev)

def tcdf (lower, upper, df, mean=0, stdev=1):
    return t.cdf(upper, df, mean, stdev) - t.cdf(lower, df, mean, stdev)

def tinv (p, df, mean=0, stdev=1):
    return t.ppf(p, df, mean, stdev)

def binompdf (n, p, x):
    return binom.pmf(x, n, p)

def binomcdf (n, p, x):
    return binom.cdf(x, n, p)

def binommean (n, p):
    return binom.mean(n, p)

def binomstdev (n, p):
    return binom.stdev(n, p)

def mean (data, weights=[]):
    if len(weights) == 0:
        return np.mean(data)
    else:
        return np.average(data, weights=weights)

def stdevp (data, weights=[]):
    if len(weights) == 0:
        return np.std(data)
    else:
        wavg = np.average(data, weights=weights)
        wvariance = np.average((data-wavg)**2, weights=weights)
    return math.sqrt(wvariance)
    
def stdev (data, weights=[]):
    n = len(data)
    return stdevp(data, weights) * math.sqrt(n/(n-1))

def linreg(x_data, y_data):
    result = linregress(x_data, y_data)
    r = result.rvalue
    #p = result.pvalue
    n = len(x_data)
    df = n - 1
    t = r * math.sqrt( (n - 2) / (1 - (r) ** 2))
    pval = 2 * tcdf( abs(t), 1E99, df)
    return (result.slope, result.intercept, result.rvalue, t, pval)

def classranges(classes, data=[], minval="", class_width=""):

    # if a data set is provided, compute the minimum value and
    #  the class width from that
    if len(data) > 0:
        minval = float(min(data))
        maxval = float(max(data))
        class_width = math.floor( ((maxval - minval) / float(classes)) )
    else:
        # reduce this by one because we generate the classes from
        #  the lcl to the ucl, not from one lcl to the next
        class_width -= 1
    
    ranges = []
    baseline = minval
    for _ in range(0, classes):
        ranges.append([ round(baseline), round(baseline + class_width) ])
        baseline += class_width + 1

    return ranges

def getclasslimits(ranges):
    lcl = []
    ucl = []
    for crange in ranges:
        lcl.append(crange[0])
        ucl.append(crange[1])
    return (lcl, ucl)

def frequencies(data, classes):
    bins = classranges(classes, data)
    freq = np.zeros(classes)
    for value in data:
        for i in range(0, len(bins)):
            bin = bins[i]
            if (float(value) >= float(bin[0])) and (float(value) <= float(bin[1])):
                freq[i] += 1
    ret_freq = []
    for value in freq:
        ret_freq.append(round(value))
    return ret_freq

def midpoints(ranges):
    midpts = []
    for crange in ranges:
        lcl, ucl = crange[0], crange[1]
        midpt = (ucl + lcl) / 2
        if (ucl + lcl) % 2 == 0:
            midpt = round(midpt)
        midpts.append(midpt)
    return midpts

def relativefreq(freq):
    total = sum(freq)
    rel_freq = []
    for val in freq:
        rel_freq.append(val / total)
    return rel_freq

def cumulativefreq(freq):
    total = 0
    cum_freq = []
    for val in freq:
        cum_freq.append(total + val)
        total += val
    return cum_freq

if __name__ == '__main__':
    stats_test()