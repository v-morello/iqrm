import itertools
import numpy as np


def shdiff(x, lag):
    """
    Returns the sequence of x[i] - x[i - lag], as an array with the same size as x.
    Boundary conditions are handled as follows:
        x[i] = x[0]   for i < 0
        x[i] = x[n-1] for i >= n, where n = len(x)
    """
    s = np.roll(x, lag)

    if lag >= 0:
        s[:lag] = x[0]
    else:
        # NOTE: lag is NEGATIVE here
        s[lag:] = x[-1]
    return x - s


def outlier_mask(x, nsigma):
    """
    Returns an outlier mask for array x. TODO: describe the method.
    """
    q1, med, q3 = np.percentile(x, [25, 50, 75])
    std = (q3 - q1) / 1.349
    return (x - med) > nsigma * std


def get_mask(s, maxlag=5, nsigma=3.0):
    """
    TODO

    Parameters
    ----------
    s : list or ndarray
        Bandpass statistic, e.g. per-channel standard deviation, from which to infer a channel mask
    maxlag : int
        Maximum shdiff lag considered for detecting outliers
    nsigma : float
        Flag as an outlier any channel for which any shdiff is further from expectation than 
        'nsigma' standard deviations.

    Returns
    -------
    mask : ndarray
        Boolean mask with the same size as the input data, where 'True' represents a bad channel
    """
    s = np.asarray(s)

    if not (isinstance(maxlag, int) and maxlag > 0):
        raise ValueError("maxlag must be an int > 0")

    nsigma = float(nsigma)
    if not nsigma > 0:
        raise ValueError("nsigma must be > 0")

    mask = np.zeros_like(s, dtype=bool)

    # Go through all lags in [-maxlag, +maxlag], except 0
    for lag in itertools.chain(range(-maxlag, 0), range(1, maxlag+1)):
        d = shdiff(s, lag)
        mask = mask | outlier_mask(d, nsigma)
    return mask
