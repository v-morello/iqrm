import numpy as np
from pytest import raises

from iqrm import iqrm_mask


def generate_noise(nchan=1024, seed=0):
    # IMPORTANT: set the random seed for reproducible results
    np.random.seed(seed)
    return np.random.normal(size=nchan)


def generate_noise_with_outlier_range(start, end, nchan=1024, seed=0):
    s = generate_noise(nchan=nchan, seed=seed)
    s[start:end] += 100
    return s


def test_param_checks():
    nchan = 1024
    s = np.zeros(nchan)

    with raises(ValueError): # radius must be > 0
        iqrm_mask(s, radius=0)

    with raises(ValueError): # radius must be an int
        iqrm_mask(s, radius=3.14)

    with raises(ValueError): # threshold must be > 0
        iqrm_mask(s, threshold=0)

    # No input elements should be inf or nan
    s[0] = np.inf
    with raises(ValueError):
        iqrm_mask(s)

    s[0] = np.nan
    with raises(ValueError):
        iqrm_mask(s)


def test_masking_noise():
    s = generate_noise()

    for maxlag in range(1, 6):
        mask = iqrm_mask(s, radius=maxlag, threshold=4.0)
        assert np.alltrue(~mask)


def test_masking_single_outlier():
    nchan = 1024
    indices = [0, 1, 42, 213, 740, 1022, 1023]

    for index in indices:
        for maxlag in range(1, 6):
            s = generate_noise_with_outlier_range(index, index+1, nchan=nchan)
            mask = iqrm_mask(s, radius=maxlag, threshold=4.0)
            assert mask[index] == True


def test_masking_outlier_range():
    nchan = 1024
    indices = [0, 1, 42, 213, 740, 1022, 1023]

    for index in indices:
        for span in range(2, 6):
            s = generate_noise_with_outlier_range(index, index+span, nchan=nchan)
            # The whole range of outliers should be masked as long as we use
            # maxlag > span
            mask = iqrm_mask(s, radius=span, threshold=4.0)
            assert np.alltrue(mask[index:index+span])