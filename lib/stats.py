from scipy.stats import norm, t, binom, linregress
import numpy as np
import math

def stats_test():
    a, b, r, t, p  = linreg([1, 2, 3, 4], [5, 6, 7, 7])
    print(f'a == {a}, b == {b}, r == {r}')

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

def mean (data):
    return np.mean(data)

def stdevp (data):
    return np.std(data)

def stdev (data):
    n = len(data)
    return np.std(data) * math.sqrt(n/(n-1))

def linreg(x_data, y_data):
    result = linregress(x_data, y_data)
    r = result.rvalue
    p = result.pvalue
    n = len(x_data)
    df = n - 1
    t = r * math.sqrt( (n - 2) / (1 - (r) ** 2))
    pval = 2 * tcdf( abs(t), 1E99, df)
    return (result.slope, result.intercept, result.rvalue, t, pval)

if __name__ == '__main__':
    stats_test()