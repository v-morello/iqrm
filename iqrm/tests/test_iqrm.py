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


def test_masking_noise():
    s = generate_noise()

    for radius in range(1, 6):
        mask, __ = iqrm_mask(s, radius=radius, threshold=4.0)
        assert np.alltrue(~mask)


def test_masking_single_outlier():
    nchan = 1024
    indices = [0, 1, 42, 213, 740, 1022, 1023]

    for index in indices:
        # NOTE: when using radius = 1, if the either the first or last element are the sole 
        # outlier, they won't be detected (the single vote they receive is not valid). 
        # We thus start at radius=2.
        for radius in (2, 3, 4, 6, 9):
            s = generate_noise_with_outlier_range(index, index+1, nchan=nchan)
            mask, __ = iqrm_mask(s, radius=radius, threshold=4.0)
            assert mask[index] == True


def test_masking_outlier_range():
    # The idea here is to generate data that looks like a top hat, i.e. noise plus a contiguous
    # range of high ouliers with similar values.

    # If the edges of the top-hat lie "far away" from the edges of the input array, then we expect
    # all outliers to be masked as long as:
    # max trial lag value > width

    # NOTE: for a top-hat that lies at the edge of the input array, the situation is different,
    # and the radius required to mask all outliers is such that:
    # max trial lag value > 2*width

    nchan = 1024
    indices = [67, 213, 486, 740, 959]
    trial_lag_sequence = (1, 2, 3, 4, 6, 9, 13)

    for index in indices:
        for jj, width in enumerate(trial_lag_sequence[:-1]):
            s = generate_noise_with_outlier_range(index, index+width, nchan=nchan)
            radius = trial_lag_sequence[jj+1]
            mask, __ = iqrm_mask(s, radius=radius, threshold=4.0)
            assert np.alltrue(mask[index:index+width])