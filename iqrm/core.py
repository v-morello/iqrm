import itertools
import numpy as np


def lagged_diff(x, k):
    """
    Returns the sequence of x[i] - x[i - k], as an array with the same size as x.
    Boundary conditions are handled as follows:
        x[i] = x[0]    if i < 0
        x[i] = x[n-1]  if i >= n, where n = len(x)
    """
    s = np.roll(x, k)
    if k >= 0:
        s[:k] = x[0]
    else:
        s[k:] = x[-1] # NOTE: lag is negative here
    return x - s


def outlier_mask(x, threshold=3.0):
    """
    Returns an outlier mask for array x, based on Tukey's rule and assuming that the inlier
    distribution of x (the distribution of 'good' values) is Gaussian. 'threshold' represents a
    number of Gaussian sigmas.
    """
    q1, med, q3 = np.percentile(x, [25, 50, 75])
    std = (q3 - q1) / 1.349
    return (x - med) > threshold * std


def iqrm_mask(x, radius=5, threshold=3.0):
    """
    Compute an IQRM mask for one-dimensional input data x.

    The process consists of identifying array indices i such that x[i] is significantly larger than
    at least one of its neighbours within 'radius' elements inclusive. This means calculating the 
    set of x[i] - x[i - k] for all i, and for all k in the range [-radius, +radius] except 0.

    The input 'x' can represent either
    * The per-channel standard deviation of a block of time-frequency data. Other statistics can 
      in principle be used, as long as *larger* values are expected for interference-contaminated 
      channels. In this case, the function detects bad frequency channels in the block.
    * A zero-DM time series, i.e. a block of time-frequency data integrated along the frequency
      axis. In this case, the function detects bad time samples in the block.

    Parameters
    ----------
    x : list or ndarray
        Input data (1-dimensional)
    radius : int, optional
        Radius in number of elements
    threshold : float, optional
        Flagging threshold in number of Gaussian sigmas

    Returns
    -------
    mask : ndarray
        Boolean mask with the same size as the input 'x', where 'True' denotes an outlier
    """
    x = np.asarray(x)

    if not (isinstance(radius, int) and radius > 0):
        raise ValueError("radius must be an int > 0")

    threshold = float(threshold)
    if not threshold > 0:
        raise ValueError("threshold must be > 0")

    mask = np.zeros_like(x, dtype=bool)

    # Go through all lags in [-maxlag, +maxlag], except 0
    for lag in itertools.chain(range(-radius, 0), range(1, radius+1)):
        d = lagged_diff(x, lag)
        mask = mask | outlier_mask(d, threshold)
    return mask
