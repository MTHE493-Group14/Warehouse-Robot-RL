from math import factorial

def nCr(n, r):
    """
    Determine the number of combinations that r objects can form out of a set
    of n objects.

    Parameters
    ----------
    n : int
        The number of objects chosen from.
    r : int
        The number of objects chosen.

    Returns
    -------
    int
        The number of combinations that r objects can form out of a set
        of n objects.

    """
    return int(factorial(n) / factorial(r) / factorial(n-r))