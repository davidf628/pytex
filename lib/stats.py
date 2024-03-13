from scipy.stats import norm, t, binom
import numpy as np
import math

def stats_test():
    print(stdev([1,2,3,4]))

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

if __name__ == '__main__':
    stats_test()