import itertools
import numpy as np

from collections import defaultdict


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


def genlags(radius, geofactor=1.5):
    lag = 1
    while lag <= radius:
        yield lag
        yield -lag
        lag = max(int(geofactor * lag), lag + 1)


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


def iqrm_mask2(x, radius=5, threshold=3.0):
    """
    Same as iqrm_mask(), but with voting method that prevents low channels from masking all their
    neighbours.
    """
    x = np.asarray(x)
    n = len(x)

    if not (isinstance(radius, int) and radius > 0):
        raise ValueError("radius must be an int > 0")

    threshold = float(threshold)
    if not threshold > 0:
        raise ValueError("threshold must be > 0")

    # These data structures both represent a directed graph
    # votes_cast[i] contains the recipients of votes cast by i
    # votes_received[i] contains the casters of votes received by i
    votes_cast = defaultdict(set)
    votes_received = defaultdict(set)

    for lag in genlags(radius):
        d = lagged_diff(x, lag)
        m = outlier_mask(d, threshold)

        # m[i] = True  <=> point j = i - lag cast a vote on i
        #              <=> point i received a vote from j = i - lag
        I = np.where(m)[0]
        J = np.clip(I - lag, 0, n - 1)

        for i, j in zip(I, J):
            votes_cast[j].add(i)
            votes_received[i].add(j)

    mask = np.zeros_like(x, dtype=bool)
    
    # i gets masked by j if both the following conditions are True:
    # 1) j has cast a vote on i
    # 2) j has cast strictly less votes in total than i has received in total
    for i, casters in votes_received.items():
        for j in casters:
            if j in votes_cast and len(votes_cast[j]) < len(votes_received[i]):
                mask[i] = True
                break

    return mask, dict(votes_cast)
