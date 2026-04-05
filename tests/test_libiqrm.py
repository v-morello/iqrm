"""Tests for the libiqrm C++ extension module."""

import pytest
from iqrm.libiqrm import add


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1.0, 2.0, 3.0),
        (-1.5, 2.5, 1.0),
        (0.0, 0.0, 0.0),
        (1e308, 0.0, 1e308),
    ],
)
def test_add(a, b, expected):
    """Test that add correctly sums two double-precision floats."""
    assert add(a, b) == expected
