import numpy as np
from pytest import raises

import iqrm


def generate_data(nchan=1024, seed=0):
    np.random.seed(seed)
    return np.random.normal(size=nchan)


def test_param_checks():
    pass


def test_masking():
    s = generate_data()
    mask = iqrm.get_mask(s)
    assert np.allclose(mask, np.ones_like(s))
