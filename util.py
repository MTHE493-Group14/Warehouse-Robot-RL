from math import factorial

def nCr(n, r):
    return int(factorial(n) / factorial(r) / factorial(n-r))

def nPr(n, r):
    return int(factorial(n) / factorial(n-r))