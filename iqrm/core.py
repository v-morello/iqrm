import numpy as np


def get_mask(s, maxlag=3, nsigma=3.0):
    """
    TODO

    Parameters
    ----------
    s : list or ndarray
    maxlag : int
    nsigma : float
    """
    if not (isinstance(maxlag, int) and maxlag > 0):
        raise ValueError("maxlag must be an int > 0")

    nsigma = float(nsigma)
    if not nsigma > 0:
        raise ValueError("nsigma must be > 0")

    return np.ones_like(s)